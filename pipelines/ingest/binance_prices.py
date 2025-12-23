import requests
import pandas as pd
from datetime import datetime, timezone

SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "USDC": "USDCUSDT",
}

BINANCE_BASE = "https://api.binance.us"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WITIN-DeFi-Intelligence/1.0)",
    "Accept": "application/json",
}

def fetch_prices_usdt() -> pd.DataFrame:
    """
    Lấy giá lastPrice theo USDT từ Binance.
    Output schema: asset_symbol, price_usd (dùng USDT proxy), ts_utc, source, quote
    """
    url = f"{BINANCE_BASE}/api/v3/ticker/price"

    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    data = r.json()  
    lookup = {row["symbol"]: row["price"] for row in data}

    ts = datetime.now(timezone.utc).isoformat()
    rows = []

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
