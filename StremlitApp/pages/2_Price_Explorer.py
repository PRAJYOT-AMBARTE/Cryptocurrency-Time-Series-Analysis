import streamlit as st
from utils.data_loader import load_forecast
from utils.constants import COINS, MODELS
from utils.charts import line_chart

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Price Explorer", layout="wide")

# ---------------- UI CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0b1220;
    color: #e5e7eb;
}

/* Headings */
h1 { color: #22d3ee; }
h2, h3 { color: #38bdf8; }

/* Control boxes */
.stSelectbox, .stMultiSelect {
    background-color: #020617;
}

/* Section container */
.section-box {
    background: #020617;
    border: 1.5px solid #1e293b;
    border-left: 6px solid #22d3ee;
    padding: 20px;
    border-radius: 14px;
    margin-top: 20px;
}

/* Chart container */
[data-testid="stPlotlyChart"] {
    background: #020617;
    border: 1.5px solid #38bdf8;
    border-radius: 14px;
    padding: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 2px solid #22d3ee;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📈 Price Explorer")
st.caption("Explore forecast trends for any cryptocurrency")

# ---------------- LOAD DATA ----------------
df = load_forecast()

# ---------------- CONTROLS ----------------
st.markdown("""
<div class="section-box">
    <h3>🎛️ Filters</h3>
</div>
""", unsafe_allow_html=True)

coin = st.selectbox("Select Cryptocurrency", list(COINS.keys()))

models = st.multiselect(
    "Select Models",
    MODELS,
    default=["ARIMA", "SARIMA", "PROPHET", "LSTM"]
)

# ---------------- FILTER ----------------
filtered = df[
    (df["crypto"] == coin) &
    (df["model"].isin(models))
]

if filtered.empty:
    st.warning("No data available for selected filters")
    st.stop()

# ---------------- CHART ----------------
st.markdown("""
<div class="section-box">
    <h3>📊 Forecast Trend</h3>
</div>
""", unsafe_allow_html=True)

fig = line_chart(
    filtered,
    title=f"{COINS[coin]} ({coin}) – Forecast Trends"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- DATA ----------------
with st.expander("📂 View Forecast Data"):
    st.dataframe(
        filtered.sort_values("date"),
        use_container_width=True
    )
