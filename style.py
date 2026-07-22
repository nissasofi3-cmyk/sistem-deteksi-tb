import streamlit as st
import base64


def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()


def load_css(login=False):

    bg = get_base64("rsud soeselo.jpeg")


    # ============================
    # BACKGROUND LOGIN / APP
    # ============================

    if login:

        background = f"""
        [data-testid="stAppViewContainer"]{{
            background-image:
            linear-gradient(
                rgba(255,255,255,0.65),
                rgba(255,255,255,0.65)
            ),
            url("data:image/jpeg;base64,{bg}");

            background-size:cover;
            background-position:center;
            background-repeat:no-repeat;
            background-attachment:fixed;
        }}
        """

    else:

        background = """
        [data-testid="stAppViewContainer"]{
            background:#f0fdfa;
        }
        """


    st.markdown(f"""
    <style>


    /* BACKGROUND */
    {background}


    .main {{
        background:transparent;
    }}


    .stApp {{
        background:transparent;
    }}


    /* HEADER */
    .header-box{{
        background:linear-gradient(
            90deg,
            #0F766E,
            #0891B2
        );

        padding:25px;
        border-radius:15px;
        color:white;
        text-align:center;
        margin-bottom:20px;
    }}



    /* CARD UMUM */
    .metric-card{{
        background:white;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:
        0 3px 10px rgba(0,0,0,.15);
    }}



    /* HASIL PREDIKSI */
    .result-tb{{
        background:#ffebee;
        border-left:8px solid red;
        padding:20px;
        border-radius:12px;
    }}



    .result-nontb{{
        background:#e8f5e9;
        border-left:8px solid green;
        padding:20px;
        border-radius:12px;
    }}




    /* HEADER STREAMLIT */
    [data-testid="stHeader"]{{
        background:transparent;
    }}




    /* INPUT */
    .stTextInput input{{
        border-radius:8px;
        height:42px;
    }}




    /* BUTTON */
    .stButton button{{
        width:100%;
        height:45px;
        border:none;
        border-radius:8px;

        background:#0F766E;

        color:white;
        font-weight:bold;
    }}



    .stButton button:hover{{
        background:#115e59;
        color:white;
    }}




    /* LOGIN BOX */
    div[data-testid="stVerticalBlockBorderWrapper"]{{
        background:rgba(255,255,255,.95);

        border-radius:20px;

        padding:25px;

        box-shadow:
        0 10px 30px rgba(0,0,0,.30);

        max-width:420px;

        margin:auto;

        margin-top:80px;
    }}




    /* METRIC DASHBOARD */
    .stMetric{{
        background:white;

        padding:18px;

        border-radius:18px;

        border-top:5px solid #0F766E;

        box-shadow:
        0 5px 20px rgba(0,0,0,.12);
    }}



    .stMetric:hover{{
        transform:translateY(-4px);
        transition:.3s;
    }}




    /* TABLE */
    .stDataFrame{{
        border-radius:15px;
    }}



    </style>
    """, unsafe_allow_html=True)