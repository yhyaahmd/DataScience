# evaluation.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Poppins', 'DejaVu Sans']

def show_evaluation(result):
    st.header("📊 Evaluation")

    st.write(f"**R² Score:** {result['r2']:.4f}")
    st.write(f"**MSE:** {result['mse']:.4f}")
    st.write(f"**RMSE:** {result['rmse']:.4f}")
    st.write(f"**MAE:** {result['mae']:.4f}")

    # ================= DATAFRAME =================
    df_pred = pd.DataFrame({
        "Aktual": result["y_test"].values,
        "Prediksi": result["y_pred"]
    })

    st.subheader("📋 Perbandingan Aktual vs Prediksi")
    st.dataframe(df_pred)

    # ================= VISUAL (2 WARNA) =================
    fig2, ax = plt.subplots()

    sns.scatterplot(
        x=df_pred["Aktual"],
        y=df_pred["Prediksi"],
        hue=df_pred["Prediksi"] >= df_pred["Aktual"],
        palette={True: "blue", False: "orange"},
        ax=ax,
        legend=False
    )

    fig2.suptitle(
        "Scatter Plot Perbandingan Nilai Aktual dan Prediksi",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Nilai Aktual")
    ax.set_ylabel("Nilai Prediksi")

    st.pyplot(fig2)

    # ================= KOEFISIEN =================
    st.subheader("📐 Koefisien Regresi")
    st.dataframe(result["coef"])
