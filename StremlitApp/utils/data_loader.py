import pandas as pd
import os

DATA_DIR = "data"
MASTER_FILE = "final_crypto_forecast_master.csv"

def load_forecast():
    """
    Load and clean forecast master dataset
    """
    path = os.path.join(DATA_DIR, MASTER_FILE)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{MASTER_FILE} not found in data folder")

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "forecast_price", "crypto", "model"])

    return df
