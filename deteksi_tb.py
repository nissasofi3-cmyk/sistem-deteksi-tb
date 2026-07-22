import streamlit as st
import pandas as pd


def deteksi_tb(cursor, conn, model):

    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#0F766E,#0891B2);
    padding:15px;
    border-radius:10px;
    color:white;
    margin-bottom:15px;
    width:60%;
    margin-left:0;
    margin-right:auto;
    ">
    <h2 style="margin-bottom:5px;">
    🫁 Prediksi TB Paru
    </h2>

    <p style="margin:0;">
    Analisis risiko Tuberkulosis Paru menggunakan Machine Learning (Random Forest).
    </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.data_pasien:
        st.warning("Silakan input data pasien terlebih dahulu.")
        return

    pasien = st.session_state.data_pasien

    kiri, kanan = st.columns([2,1])

    # ===========================
    # DATA PASIEN
    # ===========================
    with kiri:

        st.markdown("""
        <div style="
        background:white;
        border:2px solid #0EA5A8;
        border-radius:20px;
        padding:10px;
        width:50%;
        margin-left:0;
        margin-right:auto;
        ">
        <h2 style="
        color:#4FD1C5;
        margin:0;">
        Data Pasien
        </h2>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.text_input("Nama", pasien["nama"], disabled=True)
            st.text_input("Umur", pasien["umur"], disabled=True)
            st.text_input("Jenis Kelamin", pasien["jk"], disabled=True)
            st.text_input("Sesak Nafas", pasien["sesak"], disabled=True)

        with c2:
            st.text_input("Batuk", pasien["batuk"], disabled=True)
            st.text_input("Demam", pasien["demam"], disabled=True)
            st.text_input("Mual Muntah", pasien["mual"], disabled=True)
            st.text_input("Penyakit Bawaan", pasien["penyakit"], disabled=True)
        
        st.write("")

        proses = st.button("🔍 Proses Prediksi")

        st.markdown("</div>", unsafe_allow_html=True)


    # ===========================
    # PROSES PREDIKSI
    # ===========================
    if proses:

        input_model = pd.DataFrame([[
            pasien["umur"],
            0 if pasien["jk"] == "L" else 1,
            1 if pasien["sesak"] == "Ya" else 0,
            1 if pasien["batuk"] == "Ya" else 0,
            1 if pasien["demam"] == "Ya" else 0,
            1 if pasien["mual"] == "Ya" else 0,
            1 if pasien["penyakit"] == "Ya" else 0
        ]], columns=[
            "Umur",
            "Jenis Kelamin",
            "Sesak Nafas",
            "Batuk",
            "Demam",
            "Mual Muntah",
            "Penyakit Bawaan"
        ])

        hasil = model.predict(input_model)[0]
        prob = model.predict_proba(input_model)[0]

        cursor.execute("""
        SELECT id_pasien
        FROM pasien
        ORDER BY id_pasien DESC
        LIMIT 1
        """)

        id_pasien = cursor.fetchone()[0]

        hasil_prediksi = "TB Paru" if hasil == 1 else "Tidak TB"
        probabilitas = round(prob[1] * 100, 2)

        cursor.execute("""
        INSERT INTO hasil_deteksi
        (id_pasien, hasil_prediksi, probabilitas, tanggal_deteksi)
        VALUES (?,?,?,datetime('now'))
        """, (id_pasien, hasil_prediksi, probabilitas))

        conn.commit()

        st.divider()

        st.subheader("📊 Hasil Prediksi")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Probabilitas TB Paru",
                f"{round(prob[1]*100,2)} %"
            )

            st.progress(int(prob[1]*100))

        with col2:

            st.metric(
                "Probabilitas Tidak TB",
                f"{round(prob[0]*100,2)} %"
            )

        st.write("")

        if hasil == 1:

            st.markdown(f"""
            <div style="
            background:#FEE2E2;
            border-left:8px solid #DC2626;
            padding:25px;
            border-radius:15px;">

            <h2 style="color:#B91C1C;">
            ⚠️ TERINDIKASI TB PARU
            </h2>

            <h3>
            Probabilitas : {probabilitas}%
            </h3>

            <p>
            Pasien disarankan menjalani pemeriksaan lanjutan
            oleh tenaga kesehatan.
            </p>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div style="
            background:#DCFCE7;
            border-left:8px solid #16A34A;
            padding:25px;
            border-radius:15px;">

            <h2 style="color:#15803D;">
            ✅ TIDAK TERINDIKASI TB PARU
            </h2>

            <h3>
            Probabilitas : {100-probabilitas:.2f}%
            </h3>

            <p>
            Berdasarkan model Machine Learning,
            pasien tidak menunjukkan indikasi TB Paru.
            </p>

            </div>
            """, unsafe_allow_html=True)
