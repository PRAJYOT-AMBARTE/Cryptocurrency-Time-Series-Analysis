import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils.data_loader import load_forecast
from utils.constants import COINS, MODELS
from utils.charts import line_chart

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Model Comparison",
    page_icon="📊",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.block-container { padding-top: 1.2rem; }

.live-card {
    background: linear-gradient(135deg, #111827, #1f2937);
    border-left: 6px solid #2563eb;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.live-title {
    font-size: 17px;
    font-weight: 700;
    color: #e5e7eb;
}
.live-price {
    font-size: 32px;
    font-weight: 800;
    color: #22c55e;
}
.live-meta {
    color: #9ca3af;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- BINANCE LIVE PRICE ----------------
BINANCE_SYMBOL = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "ADA": "ADAUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
    "DOGE": "DOGEUSDT",
    "DOT": "DOTUSDT",
    "LTC": "LTCUSDT"
}

def fetch_live_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=5).json()
        return float(r["price"])
    except:
        return None

# ---------------- TITLE ----------------
st.title("📊 Model Comparison")
st.caption("Compare ARIMA, SARIMA, Prophet & LSTM forecasts with LIVE market price")

# ---------------- LOAD DATA ----------------
df = load_forecast()

# ---------------- CONTROLS ----------------
coin = st.selectbox("Select Cryptocurrency", list(COINS.keys()))

models = st.multiselect(
    "Select Models",
    MODELS,
    default=[m for m in MODELS if m != "LIVE"]
)

# ---------------- LIVE PRICE CARD ----------------
live_price = fetch_live_price(BINANCE_SYMBOL.get(coin))
if live_price:
    st.markdown(f"""
    <div class="live-card">
        <div class="live-title">🔴 Live {COINS[coin]} ({coin}) Price</div>
        <div class="live-price">${live_price:,.4f}</div>
        <div class="live-meta">
            Source: Binance • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FILTER DATA ----------------
filtered = df[
    (df["crypto"] == coin) &
    (df["model"].isin(models))
]

if filtered.empty:
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# ---------------- MODEL COMPARISON CHART ----------------
fig = line_chart(
    filtered,
    title=f"{COINS[coin]} ({coin}) – Model Comparison"
)

# IMPORTANT: force readable chart colors
fig.update_layout(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    xaxis=dict(
        title=dict(text="Date", font=dict(color="#111827")),
        tickfont=dict(color="#111827"),
        gridcolor="#e5e7eb"
    ),
    yaxis=dict(
        title=dict(text="Price (USD)", font=dict(color="#111827")),
        tickfont=dict(color="#111827"),
        gridcolor="#e5e7eb"
    ),
    legend=dict(font=dict(color="#111827"))
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- KPIs ----------------
st.subheader("📌 Latest Forecast Values")

latest = (
    filtered
    .sort_values("date")
    .groupby("model")
    .tail(1)
)

cols = st.columns(len(latest))
for col, (_, row) in zip(cols, latest.iterrows()):
    col.metric(
        label=row["model"],
        value=f"${row['forecast_price']:,.2f}"
    )

# ---------------- DATA TABLE ----------------
with st.expander("📂 View Comparison Data"):
    st.dataframe(
        filtered.sort_values(["model", "date"]),
        use_container_width=True
    )
