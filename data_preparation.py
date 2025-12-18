import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import MinMaxScaler, StandardScaler

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Poppins', 'DejaVu Sans']

# ===============================
# 1. MISSING VALUE (MODUS)
# ===============================
def handle_missing_value(df):
    df = df.copy()
    info = {}

    missing_before = df.isnull().sum()
    info["missing_before"] = missing_before

    handled_columns = []

    for col in df.columns:
        if missing_before[col] > 0:
            modus = df[col].mode()[0]
            df[col] = df[col].fillna(modus)

            handled_columns.append({
                "Kolom": col,
                "Tipe Data": str(df[col].dtype),
                "Metode": "Modus",
                "Nilai Pengganti": modus,
                "Jumlah Missing Value": missing_before[col]
            })

    info["missing_after"] = df.isnull().sum()
    info["handled_columns"] = pd.DataFrame(handled_columns)

    return df, info


# ===============================
# 2. OUTLIER (IQR → MEDIAN)
# ===============================
def count_outlier_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 2.5 * IQR
    upper = Q3 + 2.5 * IQR
    return ((df[col] < lower) | (df[col] > upper)).sum()


def replace_outlier_with_median(df, show_plot=False):
    df = df.copy()
    num_cols = df.select_dtypes(include=np.number).columns
    num_cols = [c for c in num_cols if c != "Tahun"]

    laporan = []

    for col in num_cols:
        outlier_before = count_outlier_iqr(df, col)

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 2.5 * IQR
        upper = Q3 + 2.5 * IQR
        median = df[col].median()

        df[col] = np.where(
            (df[col] < lower) | (df[col] > upper),
            median,
            df[col]
        )

        outlier_after = count_outlier_iqr(df, col)

        laporan.append({
            "Kolom": col,
            "Outlier Sebelum": outlier_before,
            "Outlier Sesudah": outlier_after
        })

    fig = None
    if show_plot and len(num_cols) > 0:
        fig, ax = plt.subplots(len(num_cols), 1, figsize=(10, 5 * len(num_cols)))
        if len(num_cols) == 1:
            ax = [ax]

        for i, col in enumerate(num_cols):
            sns.boxplot(x=df[col], ax=ax[i], whis=2.5)
            ax[i].set_title(f"Boxplot {col} (Median)")

    return df, pd.DataFrame(laporan), fig


# ===============================
# 3. SCALING
# ===============================
def normalize_data(df):
    scaler = MinMaxScaler()
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df


def standardize_data(df):
    scaler = StandardScaler()
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df


# ===============================
# 4. STREAMLIT FLOW
# ===============================
def prepare_data(df):
    st.header("🧹 Data Preparation")

    df_clean, info = handle_missing_value(df)

    st.subheader("Missing Value")
    st.dataframe(info["missing_before"])
    st.dataframe(info["handled_columns"])
    st.dataframe(info["missing_after"])

    show_plot = st.checkbox("Tampilkan Boxplot Outlier")
    df_no_outlier, laporan, fig = replace_outlier_with_median(df_clean, show_plot)

    st.subheader("Outlier")
    st.dataframe(laporan)
    if fig:
        st.pyplot(fig)

    metode = st.radio("Metode Skala:", ["Normalisasi", "Standarisasi"])
    df_ready = normalize_data(df_no_outlier) if metode == "Normalisasi" else standardize_data(df_no_outlier)

    st.subheader("Data Siap Modeling")
    st.dataframe(df_ready.head())

    return df_ready