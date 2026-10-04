import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Backtesting",
    page_icon="📉",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}
.backtest-box {
    border: 2px solid #2563eb;
    border-radius: 14px;
    padding: 18px;
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
st.title("📉 Strategy Backtesting & Performance")
st.caption("Evaluate a simple trend-following strategy using forecasted prices")

# ---------------- CONTROLS ----------------
coin = st.selectbox("Select Cryptocurrency", sorted(df["crypto"].unique()))
model = st.selectbox("Select Model", sorted(df["model"].unique()))

coin_df = df[
    (df["crypto"] == coin) &
    (df["model"] == model)
].sort_values("date").copy()

if len(coin_df) < 20:
    st.warning("Not enough data for backtesting")
    st.stop()

# =================================================
# 🔁 STRATEGY LOGIC
# =================================================
# Buy if price increases, Sell if price decreases
coin_df["signal"] = np.where(
    coin_df["forecast_price"].diff() > 0, 1, -1
)

coin_df["returns"] = coin_df["forecast_price"].pct_change()
coin_df["strategy_returns"] = coin_df["signal"].shift(1) * coin_df["returns"]

coin_df = coin_df.dropna()
coin_df["equity_curve"] = (1 + coin_df["strategy_returns"]).cumprod()

# =================================================
# 📈 EQUITY CURVE
# =================================================
st.subheader("📈 Strategy Equity Curve")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=coin_df["date"],
    y=coin_df["equity_curve"],
    mode="lines",
    line=dict(color="#22c55e", width=3),
    name="Equity Curve"
))

fig.update_layout(
    template="plotly_dark",
    height=420,
    plot_bgcolor="#0f172a",
    paper_bgcolor="#0f172a",
    xaxis_title="Date",
    yaxis_title="Portfolio Value",
    hovermode="x unified"
)

st.markdown('<div class="backtest-box">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# 📊 PERFORMANCE METRICS
# =================================================
st.subheader("📊 Performance Metrics")

total_return = (coin_df["equity_curve"].iloc[-1] - 1) * 100
max_loss = coin_df["strategy_returns"].min() * 100

sharpe_ratio = 0.0
if coin_df["strategy_returns"].std() != 0:
    sharpe_ratio = (
        coin_df["strategy_returns"].mean()
        / coin_df["strategy_returns"].std()
    ) * np.sqrt(365)

c1, c2, c3 = st.columns(3)

c1.metric("Total Return", f"{total_return:.2f}%")
c2.metric("Max Strategy Loss", f"{max_loss:.2f}%")
c3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

st.caption(
    "Sharpe Ratio > 1 = good | > 2 = very good • Strategy uses forecast trend direction"
)

# ---------------- RAW DATA ----------------
with st.expander("📂 View Backtesting Data"):
    st.dataframe(
        coin_df[[
            "date",
            "forecast_price",
            "signal",
            "returns",
            "strategy_returns",
            "equity_curve"
        ]],
        use_container_width=True
    )
