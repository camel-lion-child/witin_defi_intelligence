"""I fetch real-time crypto prices from Binance, standardize them into a structured dataset, and timestamp the data for downstream analytics.

Cette fonction récupère les prix crypto en temps réel depuis Binance, les standardise dans un format structuré et ajoute un timestamp pour l’analyse."""

import requests
import pandas as pd
from datetime import datetime, timezone
#mapping internal asset symbol: Binance trading pairs
SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "USDC": "USDCUSDT",
}

BINANCE_BASE = "https://api.binance.us" #Binance US API base URL

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WITIN-DeFi-Intelligence/1.0)",
    "Accept": "application/json",
}

def fetch_prices_usdt() -> pd.DataFrame:
    """
    take lastPrice in USDT from Binance.
    Output schema: asset_symbol, price_usd (using USDT proxy), ts_utc, source, quote
    """
    url = f"{BINANCE_BASE}/api/v3/ticker/price" #endpoint for latest ticker prices

    r = requests.get(url, headers=HEADERS, timeout=20) #call Binance API
    r.raise_for_status()

    data = r.json()  #convert response into lookup dictionary (symbol - price)
    lookup = {row["symbol"]: row["price"] for row in data}

    ts = datetime.now(timezone.utc).isoformat() #generate current tiemstamp (data freshness)
    rows = []
    #build standardized dataset
    for asset, bin_symbol in SYMBOLS.items():
        price = lookup.get(bin_symbol)
        rows.append(
            {
                "asset_symbol": asset,
                "price_usd": float(price) if price is not None else None,
                "ts_utc": ts,
                "source": "binance",
                "quote": "USDT",
            }
        )

    return pd.DataFrame(rows)
