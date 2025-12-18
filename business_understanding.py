# business_understanding.py
import streamlit as st


def show_business_understanding():

    st.header("📌 Business Understanding")

    st.markdown("""
    ### Latar Belakang
    Sektor pertanian sangat dipengaruhi oleh faktor lingkungan seperti curah hujan,
    temperatur, kelembapan, serta karakteristik lahan dan irigasi.
    Namun, estimasi hasil pertanian masih sering dilakukan secara manual
    dan subjektif.

    ### Permasalahan
    - Sulit memprediksi hasil pertanian secara akurat  
    - Tidak diketahui faktor mana yang paling berpengaruh  
    - Perencanaan produksi menjadi tidak optimal  

    ### Tujuan Penelitian
    - Membangun model **regresi linear**  
    - Memprediksi **hasil pertanian (numerik)**  
    - Mengukur performa model dengan metrik evaluasi  

    ### Solusi
    Menggunakan pendekatan **CRISP-DM** dan model **Machine Learning**
    untuk menghasilkan prediksi yang objektif dan terukur.
    """)
