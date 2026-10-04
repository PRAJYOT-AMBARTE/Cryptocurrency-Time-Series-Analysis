import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Price Forecasting App",
    page_icon="🚀",
    layout="wide"
)

# ---------------- INBUILT CSS ----------------
st.markdown("""
<style>
/* ---------- GLOBAL ---------- */
body {
    background-color: #0b0f19;
    color: #e5e7eb;
}

h1, h2, h3 {
    color: #38bdf8;
}

/* ---------- TOP NAV BAR ---------- */
.navbar {
    background: linear-gradient(90deg, #0f172a, #020617);
    padding: 18px 30px;
    border-bottom: 2px solid #38bdf8;
    margin-bottom: 25px;
}
.navbar h1 {
    font-size: 1.8rem;
    margin: 0;
    color: #38bdf8;
    font-weight: 700;
}

/* ---------- MAIN ---------- */
.main {
    padding: 30px;
}

/* ---------- HERO ---------- */
.hero {
    text-align: center;
    padding: 50px 20px;
}
.hero h1 {
    font-size: 3rem;
    color: #f8fafc;
}
.hero p {
    font-size: 1.15rem;
    color: #cbd5e1;
}

/* ---------- CARDS ---------- */
.card {
    background: #020617;
    padding: 25px;
    border-radius: 14px;
    margin-top: 22px;
    border: 1.5px solid #1e293b;
    box-shadow: 0 0 0 1px rgba(56,189,248,0.15);
}

/* ---------- BADGES ---------- */
.badge {
    display: inline-block;
    background: #0f172a;
    padding: 8px 14px;
    border-radius: 20px;
    margin: 6px;
    font-size: 14px;
    border: 1px solid #38bdf8;
    color: #38bdf8;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 2px solid #38bdf8;
}

/* ---------- SUCCESS ---------- */
.stAlert {
    border-left: 6px solid #22c55e;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAV BAR ----------------
st.markdown("""
<div class="navbar">
    <h1>🚀 Crypto Price Forecasting Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <h1>Crypto Price Forecasting Application</h1>
    <p>
        Multi-coin forecasting using <b>ARIMA, SARIMA, Prophet & LSTM</b><br>
        Real-time price tracking & professional analytics dashboards
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURES ----------------
st.markdown("""
<div class="card">
    <h3>✨ Key Features</h3>
    <div class="badge">📈 Multi-Coin Forecasting</div>
    <div class="badge">🧠 ARIMA / SARIMA</div>
    <div class="badge">🔮 Prophet</div>
    <div class="badge">🤖 LSTM</div>
    <div class="badge">🔴 Live Prices</div>
    <div class="badge">📊 Interactive Charts</div>
</div>
""", unsafe_allow_html=True)

# ---------------- INSTRUCTIONS ----------------
st.markdown("""
<div class="card">
    <h3>🧭 How to Use</h3>
    <ul>
        <li>Select a coin from the sidebar</li>
        <li>Explore forecasts & live prices</li>
        <li>Compare models visually</li>
        <li>Analyze trends using EDA</li>
        <li>Evaluate risk & performance</li>
    </ul>
</div>
""", unsafe_allow_html=True)


