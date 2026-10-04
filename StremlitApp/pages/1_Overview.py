import streamlit as st
from utils.data_loader import load_forecast
from utils.constants import COINS, MODELS

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Overview", layout="wide")

# ---------------- UI CSS (COLORFUL + BORDERS) ----------------
st.markdown("""
<style>
/* Page background */
body {
    background-color: #0b1220;
    color: #e5e7eb;
}

/* Headings */
h1 {
    color: #38bdf8;
}
h2, h3 {
    color: #22d3ee;
}

/* KPI cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #020617, #020617);
    border: 1.5px solid #38bdf8;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 0 15px rgba(56,189,248,0.15);
}

/* Sections */
.section-box {
    background: #020617;
    border: 1.5px solid #1e293b;
    border-left: 6px solid #38bdf8;
    padding: 20px;
    border-radius: 14px;
    margin-top: 25px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 2px solid #38bdf8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📊 Project Overview")
st.caption("Quick summary of data, coins, and models")

# ---------------- LOAD DATA ----------------
df = load_forecast()

# ---------------- KPIs ----------------
total_records = len(df)
total_coins = df["crypto"].nunique()
total_models = df["model"].nunique()
date_min = df["date"].min().date()
date_max = df["date"].max().date()

c1, c2, c3, c4 = st.columns(4)
c1.metric("📁 Total Records", total_records)
c2.metric("🪙 Total Coins", total_coins)
c3.metric("🧠 Total Models", total_models)
c4.metric("📅 Date Range", f"{date_min} → {date_max}")

st.divider()

# ---------------- COINS LIST ----------------
st.markdown("""
<div class="section-box">
    <h3>🪙 Supported Cryptocurrencies</h3>
</div>
""", unsafe_allow_html=True)

st.write(", ".join([f"**{k}** ({v})" for k, v in COINS.items()]))

# ---------------- MODELS LIST ----------------
st.markdown("""
<div class="section-box">
    <h3>🧠 Forecasting Models</h3>
</div>
""", unsafe_allow_html=True)

st.write(", ".join([f"**{m}**" for m in MODELS]))

st.divider()


