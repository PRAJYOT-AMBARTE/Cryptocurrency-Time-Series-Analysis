import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Risk & Covariance",
    page_icon="⚠️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
.cov-box {
    border: 2px solid #2563eb;
    border-radius: 14px;
    padding: 20px;
    background-color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
DATA_PATH = os.path.join("data", "final_crypto_forecast_master.csv")

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["forecast_price"] = pd.to_numeric(df["forecast_price"], errors="coerce")
df = df.dropna(subset=["date", "forecast_price"])

# ---------------- TITLE ----------------
st.title("⚠️ Risk & Covariance Analysis")
st.caption("Cross-asset dependency and risk structure using covariance")

# ---------------- MODEL SELECTION ----------------
model = st.selectbox(
    "Select Forecasting Model",
    sorted(df["model"].unique())
)

# ---------------- PIVOT DATA ----------------
pivot_df = (
    df[df["model"] == model]
    .pivot_table(
        index="date",
        columns="crypto",
        values="forecast_price"
    )
    .dropna(axis=1)
)

if pivot_df.shape[1] < 2:
    st.warning("⚠️ At least 2 cryptocurrencies are required")
    st.stop()

# ---------------- COVARIANCE MATRIX ----------------
cov_matrix = pivot_df.cov()

# ---------------- STATIC HEATMAP ----------------
st.subheader(f"📊 Covariance Matrix – {model}")

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(11, 7))

sns.heatmap(
    cov_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    linewidths=0.6,
    linecolor="#1e3a8a",
    cbar_kws={"shrink": 0.8},
    ax=ax
)

ax.set_title("Asset Covariance Heatmap", fontsize=14, color="white", pad=12)
ax.tick_params(axis="x", rotation=45, colors="white")
ax.tick_params(axis="y", rotation=0, colors="white")

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color("#2563eb")
    spine.set_linewidth(1.2)

st.markdown('<div class="cov-box">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- EXPLANATION ----------------
st.caption(
    "Positive values → assets move together | "
    "Negative values → diversification benefit | "
    "Higher magnitude → higher joint risk"
)

# ---------------- RAW DATA ----------------
with st.expander("📂 View Covariance Values"):
    st.dataframe(
        cov_matrix.style.format("{:.4f}"),
        use_container_width=True
    )
