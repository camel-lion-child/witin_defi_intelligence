import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1])) #add project root to python path for local imports

import streamlit as st
import pandas as pd
import requests
from layout import setup_page

setup_page("Markets — WITIN")

BINANCE_BASE = "https://api.binance.us" #Binance Us API endpoint

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WITIN-DeFi-Intelligence/1.0)",
    "Accept": "application/json",
}

ASSETS = {
    "Bitcoin (BTC)": "BTCUSDT",
    "Ethereum (ETH)": "ETHUSDT",
    "Aave (AAVE)": "AAVEUSDT",
    "Solana (SOL)": "SOLUSDT",
    "USD Coin (USDC)": "USDCUSDT",
    "Tether (USDT)": "USDTUSDT",
    "Cardano (ADA)": "ADAUSDT",
    "XRP (XRP)": "XRPUSDT",
    "Dogecoin (DOGE)": "DOGEUSDT",
    "TRON (TRX)": "TRXUSDT",
    "Chainlink (LINK)": "LINKUSDT",
    "Uniswap (UNI)": "UNIUSDT",
    "BNB (BNB)": "BNBUSDT",
}

@st.cache_data(ttl=300)
def fetch_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    #fetch OHLCV candles from Binance and cache results for 5 mins
    url = f"{BINANCE_BASE}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    #convert raw API rrsponse into structured dataframe
    rows = []
    for k in data:
        rows.append({
            "Timestamp": pd.to_datetime(k[0], unit="ms", utc=True),
            "Open": float(k[1]),
            "High": float(k[2]),
            "Low": float(k[3]),
            "Close": float(k[4]),
            "Volume": float(k[5]),
        })
    return pd.DataFrame(rows)

def interval_and_limit(days: int):
    #use hourly candles for short windows, daily candles for longer windows
    if days <= 14:
        return "1h", min(days * 24, 1000)
    return "1d", min(days, 1000)

st.title("Markets")
st.caption("Market pulse from Binance (USDT≈USD). Clean context for research & dashboards.")

#user controls
c1, c2 = st.columns([0.35, 0.65], gap="large")
with c1:
    asset = st.selectbox("Asset", list(ASSETS.keys()))
    days = st.slider("Window (days)", 7, 180, 30)

#resolve selected trading pair & data frequency
symbol = ASSETS[asset]
interval, limit = interval_and_limit(days)

#fetch market data
try:
    df = fetch_klines(symbol, interval, limit)
except Exception as e:
    st.error(f"Failed to fetch Binance data: {e}")
    st.stop()

if df.empty: #stop if no data returned
    st.warning("No data returned. Try another asset or timeframe.")
    st.stop()

#compute simple performance metrcis
latest = df["Close"].iloc[-1]
prev = df["Close"].iloc[0]
chg = ((latest - prev) / prev) * 100 if prev else 0.0

#display KPI metrics
m1, m2, m3 = st.columns(3)
m1.metric("Latest (USDT≈USD)", f"{latest:,.2f}")
m2.metric(f"Change ({days}d)", f"{chg:,.2f}%")
m3.metric("Candle interval", interval)

st.divider()
#price chart
st.markdown("### Price trend")
st.line_chart(df.set_index("Timestamp")["Close"])
#recent raw candles
st.markdown("### Recent candles")
st.dataframe(df.tail(20), use_container_width=True, hide_index=True)
