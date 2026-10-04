import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Risk Analysis",
    page_icon="⚠️",
    layout="wide"
)

# ---------------- CUSTOM CSS (NO WHITE) ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
.risk-box {
    border: 2px solid #2563eb;
    border-radius: 12px;
    padding: 16px;
    margin-top: 10px;
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
st.title("⚠️ Volatility & Risk Analysis")
st.caption("Risk metrics derived from forecasted prices")

# ---------------- COIN SELECT ----------------
coin = st.selectbox(
    "Select Cryptocurrency",
    sorted(df["crypto"].unique())
)

coin_df = df[df["crypto"] == coin].sort_values("date")

# ---------------- RETURNS & VOLATILITY ----------------
coin_df["returns"] = coin_df["forecast_price"].pct_change()
coin_df["volatility"] = (
    coin_df["returns"]
    .rolling(30)
    .std() * np.sqrt(365)
)

# ---------------- VOLATILITY CHART ----------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=coin_df["date"],
    y=coin_df["volatility"],
    mode="lines+markers",
    line=dict(color="#ff6b6b", width=3),
    marker=dict(size=5),
    name="Volatility"
))

fig.update_layout(
    template="plotly_dark",
    height=420,
    title=f"{coin} – 30-Day Rolling Volatility",
    xaxis=dict(
        title="Date",
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Volatility",
        tickfont=dict(color="white")
    ),
    plot_bgcolor="#0f172a",
    paper_bgcolor="#0f172a",
    margin=dict(l=40, r=40, t=60, b=40)
)

st.markdown('<div class="risk-box">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RISK METRICS ----------------
st.subheader("📌 Risk Metrics Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "📉 Max Drawdown",
        f"{coin_df['returns'].min() * 100:.2f}%"
    )

with c2:
    st.metric(
        "📈 Avg Daily Return",
        f"{coin_df['returns'].mean() * 100:.2f}%"
    )

with c3:
    st.metric(
        "⚠️ Current Volatility",
        f"{coin_df['volatility'].iloc[-1]:.4f}"
    )

st.caption("Volatility is annualized • Higher volatility indicates higher risk")
