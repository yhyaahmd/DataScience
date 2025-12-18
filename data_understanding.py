# data_understanding.py
import streamlit as st
import pandas as pd
import io

def show_data_understanding(df):
    st.header("🔍 Data Understanding")

    st.write(f"Jumlah Baris: {df.shape[0]}")
    st.write(f"Jumlah Kolom: {df.shape[1]}")

    st.write("Data Head")
    st.dataframe(df.head())

    st.write("Data Tail")
    st.dataframe(df.tail())

    st.write("Informasi Struktur Data")

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    st.code(info_str)

    st.write("Statistik Deskriptif")
    st.dataframe(df.describe())
