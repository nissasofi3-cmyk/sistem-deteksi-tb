import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def dashboard(cursor):

    # ==========================
    # AMBIL DATA DATABASE
    # ==========================
    cursor.execute("SELECT COUNT(*) FROM pasien")
    total_pasien = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hasil_deteksi")
    total_deteksi = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM hasil_deteksi
    WHERE hasil_prediksi='TB Paru'
    """)
    total_tb = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM hasil_deteksi
    WHERE hasil_prediksi='Tidak TB'
    """)
    total_non_tb = cursor.fetchone()[0]

    # ==========================
    # HERO SECTION
    # ==========================
    kiri, kanan = st.columns([2,1])

    with kiri:

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#0F766E,#0891B2);
        padding:45px;
        border-radius:25px;
        color:white;
        min-height:380px;">


        <h1 style="
        color:white;
        font-size:56px;
        line-height:1.15;
        margin-top:20px;">
        Sistem Deteksi Dini<br>
        Penyakit Tuberkulosis Paru<br>
        Secara Akurat
        </h1>

        <p style="
        color:#ecfeff;
        font-size:18px;">
        Sistem berbasis Machine Learning menggunakan
        algoritma Random Forest untuk membantu
        deteksi dini Tuberkulosis Paru.
        </p>

        </div>
        """, unsafe_allow_html=True)


    with kanan:

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:12px;
        margin-bottom:10px;
        box-shadow:0 5px 20px rgba(0,0,0,.15);">
        🤒 <b>Demam</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:12px;
        margin-bottom:10px;
        box-shadow:0 5px 20px rgba(0,0,0,.15);">
        😮‍💨 <b>Sesak Nafas</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:12px;
        margin-bottom:10px;
        box-shadow:0 5px 20px rgba(0,0,0,.15);">
        🩸 <b>Batuk Berdarah</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
        background:white;
        border-radius:12px;
        padding:10px;
        box-shadow:0 5px 20px rgba(0,0,0,.15);">
        🤢 <b>Mual Muntah</b>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ==========================
    # METRIC
    # ==========================
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👥 Total Pasien", total_pasien)

    with c2:
        st.metric("🫁 TB Paru", total_tb)

    with c3:
        st.metric("✅ Tidak TB", total_non_tb)

    with c4:
        st.metric("📄 Total Deteksi", total_deteksi)

    st.divider()

    # ==========================
    # GRAFIK DAN TABEL
    # ==========================
    col1, col2 = st.columns([1,2])

    with col1:

        st.subheader("Ringkasan Deteksi")

        fig, ax = plt.subplots(figsize=(4,4))

        ax.pie(
            [total_tb, total_non_tb],
            labels=["TB Paru","Tidak TB"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

    with col2:

        st.subheader("Deteksi Terbaru")

        cursor.execute("""
        SELECT
            p.nama,
            h.hasil_prediksi,
            h.probabilitas,
            h.tanggal_deteksi
        FROM hasil_deteksi h
        JOIN pasien p
        ON h.id_pasien=p.id_pasien
        ORDER BY h.id_hasil DESC
        LIMIT 5
        """)

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Nama",
                    "Hasil",
                    "Probabilitas (%)",
                    "Tanggal"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("Belum ada data deteksi.")