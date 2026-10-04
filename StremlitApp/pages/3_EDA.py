import streamlit as st
from utils.data_loader import load_forecast
from utils.constants import COINS
from utils.charts import single_model_chart

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EDA",
    page_icon="📈",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
}

/* Card with BLUE BORDER */
.chart-card {
    border: 2px solid #2563eb;   /* 🔵 Blue border */
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 20px;
    background: transparent;
}

/* Section title */
.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #e5e7eb;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📈 Exploratory Data Analysis (EDA)")
st.caption("Model-wise historical forecast trends")

# ---------------- LOAD DATA ----------------
df = load_forecast()

# ---------------- CONTROLS ----------------
coin = st.selectbox("Select Cryptocurrency", list(COINS.keys()))
coin_df = df[df["crypto"] == coin]

if coin_df.empty:
    st.warning("⚠️ No data available for selected coin")
    st.stop()

st.divider()

# ---------------- SECTION HEADER ----------------
st.markdown(
    f"<div class='section-title'>{COINS[coin]} ({coin}) – Forecast Trends by Model</div>",
    unsafe_allow_html=True
)

# ---------------- PLOTS (2x2 GRID) ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    mdf = coin_df[coin_df["model"] == "ARIMA"]
    fig = single_model_chart(mdf, "ARIMA", "ARIMA Forecast Trend")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    mdf = coin_df[coin_df["model"] == "SARIMA"]
    fig = single_model_chart(mdf, "SARIMA", "SARIMA Forecast Trend")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    mdf = coin_df[coin_df["model"] == "PROPHET"]
    fig = single_model_chart(mdf, "PROPHET", "Prophet Forecast Trend")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    mdf = coin_df[coin_df["model"] == "LSTM"]
    fig = single_model_chart(mdf, "LSTM", "LSTM Forecast Trend")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RAW DATA ----------------
with st.expander("📂 View EDA Data"):
    st.dataframe(
        coin_df.sort_values(["model", "date"]),
        use_container_width=True
    )
