import streamlit as st

def input_pasien(cursor, conn):

    kiri, kanan = st.columns([2.3,1])

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
        Form Input Data Pasien
        </h2>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        with c1:
            nama = st.text_input("Nama Pasien")

        with c2:
            umur = st.number_input(
                "Umur",
                min_value=0,
                max_value=120,
                value=0
            )

        with c3:
            jk = st.selectbox(
                "Jenis Kelamin",
                ["L", "P"]
            )

        c4, c5, c6 = st.columns(3)

        with c4:
            sesak = st.selectbox(
                "Sesak Nafas",
                ["Tidak", "Ya"]
            )

        with c5:
            batuk = st.number_input(
            "Batuk (hari)",
            min_value=0,
            max_value=365
            )

        with c6:
            demam = st.number_input(
            "Suhu Tubuh (°C)",
            min_value=35.0,
            max_value=45.0,
            step=0.1
            )

        c7, c8 = st.columns(2)

        with c7:
            mual = st.selectbox(
                "Mual Muntah",
                ["Tidak", "Ya"]
            )

        with c8:
            penyakit = st.selectbox(
                "Penyakit Bawaan",
                ["Tidak", "Ya"]
            )

        st.write("")

        if st.button("💾 Simpan Data Pasien"):

            if nama == "" or umur == 0:

                st.warning("Nama dan umur wajib diisi.")

            else:

                sql = """
                INSERT INTO pasien
                (
                    nama,
                    umur,
                    jenis_kelamin,
                    sesak_nafas,
                    batuk,
                    demam,
                    mual_muntah,
                    penyakit_bawaan
                )
                VALUES
                (?,?,?,?,?,?,?,?)
                """

                val = (
                    nama,
                    umur,
                    jk,
                    sesak,
                    batuk,
                    demam,
                    mual,
                    penyakit
                )

                cursor.execute(sql, val)
                conn.commit()

                st.session_state.data_pasien = {
                "nama": nama,
                "umur": umur,
                "jk": jk,
                "sesak": sesak,
                "batuk": batuk,
                "demam": demam,
                "mual": mual,
                "penyakit": penyakit
                }

                st.session_state.menu = "Deteksi TB Paru"
                st.rerun()
                

    with kanan:

        st.markdown("""
        <div style="
        background:#111827;
        border-radius:18px;
        padding:20px;
        color:white;
        border-left:5px solid #14B8A6;">

        <h3>📌 Instruksi</h3>

        ✔ Isi seluruh data pasien.<br><br>

        ✔ Pastikan data benar.<br><br>

        ✔ Klik tombol <b>Simpan Data Pasien</b>.<br><br>

        ✔ Lanjutkan ke menu <b>Deteksi TB Paru</b>.
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#0F766E,#14B8A6);
        border-radius:18px;
        padding:20px;
        color:white;">

        <h3>🤖 Sistem</h3>

        Model Machine Learning menggunakan algoritma
        <b>Random Forest</b> untuk melakukan prediksi
        risiko Tuberkulosis Paru.

        </div>
        """, unsafe_allow_html=True)
