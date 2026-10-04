import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Forecast Analysis",
    page_icon="📈",
    layout="wide"
)

# ---------------- CSS (NO WHITE BACKGROUND) ----------------
st.markdown("""
<style>
.block-container { padding-top: 1.2rem; }

.live-card {
    background: linear-gradient(135deg, #111827, #1f2937);
    border-left: 6px solid #2563eb;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 25px;
}
.live-title {
    font-size: 18px;
    font-weight: 700;
    color: #e5e7eb;
}
.live-price {
    font-size: 36px;
    font-weight: 800;
    color: #22c55e;
}
.live-meta {
    color: #9ca3af;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
DATA_DIR = "data"

arima_df   = pd.read_csv(os.path.join(DATA_DIR, "arima_all_coins.csv"))
sarima_df  = pd.read_csv(os.path.join(DATA_DIR, "sarima_all_coins.csv"))
prophet_df = pd.read_csv(os.path.join(DATA_DIR, "prophet_all_coins.csv"))
lstm_df    = pd.read_csv(os.path.join(DATA_DIR, "lstm_all_coins.csv"))

for d in [arima_df, sarima_df, prophet_df, lstm_df]:
    d["date"] = pd.to_datetime(d["date"], errors="coerce")

# ---------------- LIVE PRICE (BINANCE) ----------------
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
st.title("📈 Forecast Analysis")
st.caption("ARIMA • SARIMA • Prophet • LSTM • LIVE (Points + Lines)")

# ---------------- COIN SELECT ----------------
coin = st.selectbox(
    "Select Cryptocurrency",
    sorted(arima_df["crypto"].unique())
)

# ---------------- LIVE CARD ----------------
price = fetch_live_price(BINANCE_SYMBOL.get(coin))
if price:
    st.markdown(f"""
    <div class="live-card">
        <div class="live-title">🔴 Live {coin} Price</div>
        <div class="live-price">${price:,.4f}</div>
        <div class="live-meta">Source: Binance • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FILTER ----------------
def coin_filter(df):
    return df[df["crypto"] == coin].sort_values("date")

arima   = coin_filter(arima_df)
sarima  = coin_filter(sarima_df)
prophet = coin_filter(prophet_df)
lstm    = coin_filter(lstm_df)

# ---------------- PLOT FUNCTION (ERROR-FREE) ----------------
def plot_forecast(df, title, color):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["forecast_price"],
        mode="lines+markers",
        marker=dict(size=6),
        line=dict(width=3, color=color),
        name=title
    ))

    fig.update_layout(
        height=420,
        title=dict(
            text=title,
            font=dict(size=18, color="#111827")
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hovermode="x unified",
        xaxis=dict(
            title=dict(
                text="Date",
                font=dict(size=14, color="#111827")
            ),
            tickfont=dict(color="#111827"),
            gridcolor="#e5e7eb"
        ),
        yaxis=dict(
            title=dict(
                text="Price (USD)",
                font=dict(size=14, color="#111827")
            ),
            tickfont=dict(color="#111827"),
            gridcolor="#e5e7eb"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📘 ARIMA", "📙 SARIMA", "📗 Prophet", "📕 LSTM"]
)

with tab1:
    plot_forecast(arima, f"{coin} – ARIMA Forecast", "#2563eb")

with tab2:
    plot_forecast(sarima, f"{coin} – SARIMA Forecast", "#f59e0b")

with tab3:
    plot_forecast(prophet, f"{coin} – Prophet Forecast", "#22c55e")

with tab4:
    plot_forecast(lstm, f"{coin} – LSTM Forecast", "#ec4899")

# ---------------- DATA ----------------
with st.expander("📂 View Forecast Data"):
    st.dataframe(
        pd.concat([
            arima.assign(model="ARIMA"),
            sarima.assign(model="SARIMA"),
            prophet.assign(model="PROPHET"),
            lstm.assign(model="LSTM")
        ]).sort_values("date"),
        use_container_width=True
    )
