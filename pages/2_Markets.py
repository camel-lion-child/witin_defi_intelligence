import streamlit as st
import pandas as pd
import requests
from app.layout import setup_page

setup_page("Markets — WITIN")

BINANCE_BASE = "https://api.binance.com"

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
    url = f"{BINANCE_BASE}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

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
    if days <= 14:
        return "1h", min(days * 24, 1000)
    return "1d", min(days, 1000)

st.title("Markets")
st.caption("Market pulse from Binance (USDT≈USD). Clean context for research & dashboards.")

c1, c2 = st.columns([0.35, 0.65], gap="large")
with c1:
    asset = st.selectbox("Asset", list(ASSETS.keys()))
    days = st.slider("Window (days)", 7, 180, 30)

symbol = ASSETS[asset]
interval, limit = interval_and_limit(days)

try:
    df = fetch_klines(symbol, interval, limit)
except Exception as e:
    st.error(f"Failed to fetch Binance data: {e}")
    st.stop()

if df.empty:
    st.warning("No data returned. Try another asset or timeframe.")
    st.stop()

latest = df["Close"].iloc[-1]
prev = df["Close"].iloc[0]
chg = ((latest - prev) / prev) * 100 if prev else 0.0

m1, m2, m3 = st.columns(3)
m1.metric("Latest (USDT≈USD)", f"{latest:,.2f}")
m2.metric(f"Change ({days}d)", f"{chg:,.2f}%")
m3.metric("Candle interval", interval)

st.divider()

st.markdown("### Price trend")
st.line_chart(df.set_index("Timestamp")["Close"])

st.markdown("### Recent candles")
st.dataframe(df.tail(20), use_container_width=True, hide_index=True)

