import streamlit as st
import pandas as pd

from business_understanding import show_business_understanding
from data_understanding import show_data_understanding
from data_preparation import prepare_data
from modeling import run_regression
from evaluasi import show_evaluation

st.set_page_config(page_title="Prediksi Pertanian", layout="wide")

# ============================= CSS GLOBAL POPPINS & CUSTOM COLORS =============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Mengubah font untuk semua elemen */
    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stHeader, p {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Styling khusus untuk Judul Utama */
    .main-title {
        color: #2E7D32; /* Warna Hijau Daun */
        font-weight: 700;
        font-size: 42px;
        margin-bottom: 20px;
    }

    /* Mempercantik Button di Sidebar */
    div.stButton > button {
        font-family: 'Poppins', sans-serif;
        width: 100%;
        border-radius: 8px;
        transition: 0.3s;
    }
    
    /* Warna hover button agar senada dengan tema hijau */
    div.stButton > button:hover {
        border-color: #2E7D32;
        color: #2E7D32;
    }
</style>
""", unsafe_allow_html=True)
# ==============================================================================

# MENGGUNAKAN HTML UNTUK JUDUL BERWARNA HIJAU
st.markdown("<h1 class=\"main-title\">Prediksi Hasil Pertanian (CRISP-DM)</h1>", unsafe_allow_html=True)

# =============================
# INIT SESSION STATE MENU
# =============================
if "menu" not in st.session_state:
    st.session_state.menu = "Business Understanding"

# =============================
# SIDEBAR BUTTONS
# =============================
st.sidebar.title("Tahapan CRISP-DM")

if st.sidebar.button("Business Understanding", use_container_width=True):
    st.session_state.menu = "Business Understanding"

if st.sidebar.button("Data Understanding", use_container_width=True):
    st.session_state.menu = "Data Understanding"

if st.sidebar.button("Data Preparation", use_container_width=True):
    st.session_state.menu = "Data Preparation"

if st.sidebar.button("Modeling", use_container_width=True):
    st.session_state.menu = "Modeling"

if st.sidebar.button("Evaluation", use_container_width=True):
    st.session_state.menu = "Evaluation"


menu = st.session_state.menu

# =============================
# FILE UPLOADER
# =============================
uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset", type=["csv", "xlsx"]
)

df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

# =============================
# PAGE LOGIC
# =============================
if menu == "Business Understanding":
    show_business_understanding()

elif menu == "Data Understanding":
    if df is not None:
        show_data_understanding(df)
    else:
        st.warning("Upload dataset terlebih dahulu 📂")

elif menu == "Data Preparation":
    if df is not None:
        df_ready = prepare_data(df)
        st.session_state["df_ready"] = df_ready
        st.success("Data siap dipakai 🚀")
    else:
        st.warning("Upload dataset terlebih dahulu 📂")

elif menu == "Modeling":
    if "df_ready" in st.session_state:
        df_ready = st.session_state["df_ready"]

        target = st.selectbox(
            "Pilih Target (Y)",
            df_ready.select_dtypes(include="number").columns
        )

        if st.button("Jalankan Regresi"):
            result = run_regression(df_ready, target)
            st.session_state["result"] = result
            st.success("Model berhasil dilatih 🔥")
    else:
        st.warning("Lakukan Data Preparation dulu ⚙️")

elif menu == "Evaluation":
    if "result" in st.session_state:
        show_evaluation(st.session_state["result"])
    else:
        st.warning("Model belum dijalankan 🤖")