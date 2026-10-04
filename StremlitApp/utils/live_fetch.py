import requests
from datetime import datetime

BINANCE_MAP = {
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

def fetch_live_price(coin):
    symbol = BINANCE_MAP.get(coin)
    if not symbol:
        return None

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        return {
            "date": datetime.now(),
            "crypto": coin,
            "price": float(data["price"])
        }
    except:
        return None
