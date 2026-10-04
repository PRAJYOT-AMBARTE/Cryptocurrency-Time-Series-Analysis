import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Technical Indicators",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
.indicator-box {
    border: 2px solid #2563eb;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 20px;
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
st.title("📊 Technical Indicators Dashboard")
st.caption("Trend & momentum indicators based on forecasted prices")

# ---------------- CONTROLS ----------------
coin = st.selectbox("Select Cryptocurrency", sorted(df["crypto"].unique()))
model = st.selectbox("Select Model", sorted(df["model"].unique()))

coin_df = df[
    (df["crypto"] == coin) &
    (df["model"] == model)
].sort_values("date")

price = coin_df["forecast_price"]

# ---------------- RSI CALCULATION ----------------
delta = price.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
coin_df["RSI"] = 100 - (100 / (1 + rs))

# ---------------- MOVING AVERAGES ----------------
coin_df["MA_20"] = price.rolling(20).mean()
coin_df["MA_50"] = price.rolling(50).mean()

# =================================================
# 📈 PRICE + MOVING AVERAGES
# =================================================
st.subheader("📈 Price Trend with Moving Averages")

fig_price = go.Figure()

fig_price.add_trace(go.Scatter(
    x=coin_df["date"],
    y=coin_df["forecast_price"],
    mode="lines",
    name="Price",
    line=dict(color="#22c55e", width=3)
))

fig_price.add_trace(go.Scatter(
    x=coin_df["date"],
    y=coin_df["MA_20"],
    mode="lines",
    name="MA 20",
    line=dict(color="#38bdf8", dash="dot")
))

fig_price.add_trace(go.Scatter(
    x=coin_df["date"],
    y=coin_df["MA_50"],
    mode="lines",
    name="MA 50",
    line=dict(color="#facc15", dash="dash")
))

fig_price.update_layout(
    template="plotly_dark",
    height=420,
    xaxis_title="Date",
    yaxis_title="Price",
    plot_bgcolor="#0f172a",
    paper_bgcolor="#0f172a",
    hovermode="x unified"
)

st.markdown('<div class="indicator-box">', unsafe_allow_html=True)
st.plotly_chart(fig_price, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.caption("• MA20 reacts faster (short-term trend) • MA50 shows long-term trend")

# =================================================
# 📊 RSI INDICATOR
# =================================================
st.subheader("📊 Relative Strength Index (RSI)")

fig_rsi = go.Figure()

fig_rsi.add_trace(go.Scatter(
    x=coin_df["date"],
    y=coin_df["RSI"],
    mode="lines",
    name="RSI",
    line=dict(color="#a855f7", width=3)
))

# Overbought / Oversold zones
fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")

fig_rsi.update_layout(
    template="plotly_dark",
    height=360,
    xaxis_title="Date",
    yaxis_title="RSI",
    plot_bgcolor="#0f172a",
    paper_bgcolor="#0f172a",
    hovermode="x unified",
    yaxis=dict(range=[0, 100])
)

st.markdown('<div class="indicator-box">', unsafe_allow_html=True)
st.plotly_chart(fig_rsi, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.caption(
    "RSI > 70 → Overbought (sell pressure) | "
    "RSI < 30 → Oversold (buy opportunity)"
)

# ---------------- RAW DATA ----------------
with st.expander("📂 View Indicator Data"):
    st.dataframe(
        coin_df[[
            "date", "forecast_price", "MA_20", "MA_50", "RSI"
        ]].dropna(),
        use_container_width=True
    )
