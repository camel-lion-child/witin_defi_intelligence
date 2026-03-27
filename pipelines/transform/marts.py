"""I build clean analytical tables for prices, protocol snapshots, and placeholder liquidation-risk scenarios from raw DeFi market data

Construire des tables analytiques propres pour les prix, les snapshots de protocoles et 
des scénarios fictifs de risque de liquidation à partir de données brutes DeFi"""

import pandas as pd

def build_dim_prices(raw_prices: pd.DataFrame) -> pd.DataFrame:
    df = raw_prices.copy() #create a clean price dimention from raw market data
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce") #ensure price column is numeric
    df = df.dropna(subset=["asset_symbol", "price_usd", "ts_utc"]) #keep only valid rows required for analysis
    return df[["asset_symbol", "price_usd", "ts_utc"]] #return standardized output schema

def build_fact_protocol_snapshot(raw_aave: pd.DataFrame) -> pd.DataFrame:
    df = raw_aave.copy() #build a protocol level snapshot fact table from raw Aave

    df["tvl_usd"] = pd.to_numeric(df.get("tvl_usd"), errors="coerce").fillna(0.0) #standardize TVL as numeric & fill missing values
    df["protocol"] = df.get("protocol", "Aave").fillna("Aave") #default protocol name if not provided
    df["ts_utc"] = df.get("ts_utc") #keep timestamp for refresh tracking

    keep = [c for c in ["protocol", "tvl_usd", "category", "ts_utc", "source"] if c in df.columns]
    return df[keep] #return only available analytical columns

def build_fact_risk_placeholder(dim_prices: pd.DataFrame) -> pd.DataFrame:
    ts = dim_prices["ts_utc"].max() #build a placeholder risk scenario table using the latest available timestamp 
    return pd.DataFrame([
        {"scenario": "ETH -10%", "estimated_liquidatable_usd": 0.0, "ts_utc": ts},
        {"scenario": "ETH -20%", "estimated_liquidatable_usd": 0.0, "ts_utc": ts},
        {"scenario": "ETH -30%", "estimated_liquidatable_usd": 0.0, "ts_utc": ts},
    ])
