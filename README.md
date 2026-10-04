# 🚀 Cryptocurrency Time Series Analysis & Price Forecasting

## 📌 Project Overview
This project focuses on cryptocurrency price forecasting by combining historical time-series analysis, machine learning, deep learning, and real-time market data. Multiple forecasting models are implemented and compared, and their outputs are integrated into a single analytics-ready dataset and interactive dashboards.

The project is designed with industry practices, making it suitable for portfolio demonstration, resumes, and real-world analytics use cases.

## 🎯 Objectives
- Analyze historical cryptocurrency price trends
- Forecast future prices using multiple statistical and machine learning models
- Integrate live market prices via the Binance API
- Compare model outputs and evaluate performance
- Interactive visualization using a multi-page Streamlit application

## 🧠 Models Implemented
- **ARIMA** (Autoregressive Integrated Moving Average)
- **SARIMA** (Seasonal ARIMA)
- **Prophet** (Additive forecasting model by Meta)
- **LSTM** (Long Short-Term Memory Neural Networks)
- **Live Data API** (Binance API real-time ticker)

## 📂 Dataset Sources
- **Historical Data**: Kaggle cryptocurrency daily price datasets (BTC, ETH, BNB, SOL, ADA, XRP, DOGE, DOT, LTC, BCH)
- **Live Data**: Binance API (`/api/v3/ticker/price`)

## 🗂 Project Structure
```text
Cryptocurrency-Time-Series-Analysis/
├── data/
│   ├── raw/                       # Raw historical CSVs for individual coins
│   └── processed/                 # Merged and cleaned master datasets
├── notebooks/                     # Jupyter notebooks for data prep, EDA, and models
│   ├── 01_data_loading.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_multi_crypto_eda.ipynb
│   ├── 04_arima_sarima.ipynb
│   ├── 05_prophet_forecasting.ipynb
│   ├── 06_LSTM_Forecasting.ipynb
│   └── 08_final_dataset_integration.ipynb
├── StremlitApp/                   # Multi-page interactive Streamlit dashboard
│   ├── App.py                     # Main dashboard landing page
│   ├── pages/                     # Feature pages (EDA, Forecasts, Risk, Indicators, etc.)
│   ├── utils/                     # Utility modules for data loading, charts, live fetch
│   └── data/                      # Exported model forecasts and combined data
├── requirements.txt               # Python package dependencies
├── LICENSE                        # Apache 2.0 License
└── README.md                      # Project documentation
```

## ⚙️ Tech Stack
- **Languages & Libraries**: Python, Pandas, NumPy, Statsmodels, Prophet, TensorFlow / Keras, Scikit-learn
- **Data Visualization**: Matplotlib, Seaborn, Plotly
- **Web Dashboard**: Streamlit
- **APIs**: Binance REST API

## 🧪 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PRAJYOT-AMBARTE/Cryptocurrency-Time-Series-Analysis.git
   cd Cryptocurrency-Time-Series-Analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit App:**
   ```bash
   streamlit run StremlitApp/App.py
   ```

4. **Run Notebooks (Optional):**
   Execute notebooks sequentially from `01` to `08` in the `notebooks/` directory to re-generate datasets and model forecasts.

## 🏆 Key Learnings
- End-to-end time-series forecasting pipeline
- Classical time-series modeling (ARIMA / SARIMA) vs modern approaches (Prophet, LSTM)
- Live API integration with real-time price feeds
- Building interactive analytics web dashboards with Streamlit and Plotly
