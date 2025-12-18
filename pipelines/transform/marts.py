import pandas as pd

def build_dim_prices(raw_prices: pd.DataFrame) -> pd.DataFrame:
    df = raw_prices.copy()
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    df = df.dropna(subset=["asset_symbol", "price_usd", "ts_utc"])
    return df[["asset_symbol", "price_usd", "ts_utc"]]

def build_fact_protocol_snapshot(raw_aave: pd.DataFrame) -> pd.DataFrame:
    df = raw_aave.copy()
    df["tvl_usd"] = pd.to_numeric(df["tvl_usd"], errors="coerce")
    df = df.dropna(subset=["protocol", "tvl_usd", "ts_utc"])
    return df[["protocol", "tvl_usd", "category", "ts_utc"]]

def build_fact_risk_placeholder(dim_prices: pd.DataFrame) -> pd.DataFrame:
    ts = dim_prices["ts_utc"].max()
    return pd.DataFrame([
        {"scenario": "ETH -10%", "estimated_liquidatable_usd": 0.0, "ts_utc": ts},
        {"scenario": "ETH -20%", "estimated_liquidatable_usd": 0.0, "ts_utc": ts},
        {"scenario": "ETH -30%", "estimated_liquidatable_usd": 0.0, "ts_utc": ts},
    ])