import streamlit as st
import pandas as pd


def riwayat(cursor):


    cursor.execute("""
    SELECT
        p.nama,
        p.umur,
        p.jenis_kelamin,
        h.hasil_prediksi,
        h.probabilitas,
        h.tanggal_deteksi
    FROM hasil_deteksi h
    JOIN pasien p
        ON h.id_pasien = p.id_pasien
    ORDER BY h.id_hasil DESC
    """)

    data = cursor.fetchall()

    if len(data) == 0:

        st.markdown("""
        <div style="
        background:#FEF3C7;
        padding:15px;
        border-radius:10px;
        border-left:6px solid orange;">
            <h3>⚠ Belum Ada Riwayat Deteksi</h3>
            <p>Silakan lakukan deteksi pasien terlebih dahulu.</p>
        </div>
        """, unsafe_allow_html=True)

        return

    df = pd.DataFrame(
        data,
        columns=[
            "Nama Pasien",
            "Umur",
            "Jenis Kelamin",
            "Hasil Prediksi",
            "Probabilitas (%)",
            "Tanggal Deteksi"
        ]
    )

    total = len(df)
    tb = len(df[df["Hasil Prediksi"] == "TB Paru"])
    non_tb = len(df[df["Hasil Prediksi"] == "Tidak TB"])

    c0, c1, c2, c3, c4 = st.columns([1,1,1,1,1])

    with c1:
        st.metric("📄 Total Deteksi", total)

    with c2:
        st.metric("🫁 TB Paru", tb)

    with c3:
        st.metric("✅ Tidak TB", non_tb)
    st.write("")

    st.markdown("""
    <div style="
    background:white;
    border-radius:10px;
    padding:10px;
    box-shadow:0 5px 20px rgba(0,0,0,.12);">

    <h3 style="color:#0F766E;">
    📋 Data Riwayat Deteksi
    </h3>

    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
    "📥 Download Riwayat Deteksi",
    csv,
    file_name="riwayat_deteksi_tb.csv",
    mime="text/csv"
    )
    
