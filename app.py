import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

from dashboard import dashboard
from style import load_css
from input_pasien import input_pasien
from deteksi_tb import deteksi_tb
from riwayat import riwayat

st.set_page_config(
    page_title="Sistem Deteksi TB Paru",
    page_icon="🫁",
    layout="wide"
)



#koneksi Database
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_tb_paru"
)

cursor = conn.cursor()

# =====================================
# LOAD MODEL
# =====================================
try:
    model = joblib.load("model_tb_paru.pkl")
except:
    model = None


# =====================================
# SESSION STATE
# =====================================
if "login" not in st.session_state:
    st.session_state.login = False

if "data_pasien" not in st.session_state:
    st.session_state.data_pasien = {}

if "hasil_prediksi" not in st.session_state:
    st.session_state.hasil_prediksi = None

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"


# =====================================
# LOGIN PAGE
# =====================================
if not st.session_state.login:

    load_css(login=True)   # <-- TAMBAHKAN INI SAJA

    kiri, tengah, kanan = st.columns([3,2,3])

    with tengah:

        with st.container(border=True):

            st.markdown(
                "<h2 style='text-align:center;'>Sistem Deteksi TB Paru</h2>",
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Masukkan Username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Masukkan Password"
            )

            if st.button("LOG IN", use_container_width=True):
                cursor.execute(
                    "SELECT * FROM users WHERE username=%s AND password=%s",
                    (username, password)
                )

                user = cursor.fetchone()

                if user:
                    st.session_state.login = True
                    st.rerun()
                else:
                    st.error("Username atau Password salah.")
# =====================================
# MAIN APP
# =====================================
else:
    load_css(login=False)

    menu_list = [
    "Dashboard",
    "Input Data Pasien",
    "Deteksi TB Paru",
    "Riwayat Deteksi",
    "Logout"
    ]

    selected = option_menu(
        menu_title="🫁 TB Predict",
        options=menu_list,
        icons=[
        "house-fill",
        "person-plus-fill",
        "activity",
        "clock-history",
        "box-arrow-right"
        ],
        orientation="horizontal",
        default_index=menu_list.index(st.session_state.menu),
        )
    menu = selected
    # =====================================
    # MENU
    # =====================================
    if menu == "Dashboard":
        dashboard(cursor)

    elif menu == "Input Data Pasien":
        input_pasien(cursor, conn)

    elif menu == "Deteksi TB Paru":
        deteksi_tb(cursor, conn, model)

    elif menu == "Riwayat Deteksi":
        riwayat(cursor)

    elif menu == "Logout":
        st.session_state.clear()
        st.rerun()
    