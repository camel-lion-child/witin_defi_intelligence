import requests
import pandas as pd
from datetime import datetime, timezone

SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "USDC": "USDCUSDT",
}

BINANCE_BASE = "https://api.binance.com"

def fetch_prices_usdt() -> pd.DataFrame:
    """
    Lấy giá lastPrice theo USDT từ Binance.
    Output schema: asset_symbol, price_usd (dùng USDT proxy), ts_utc
    """
    url = f"{BINANCE_BASE}/api/v3/ticker/price"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()  # list of {"symbol": "...", "price": "..."}

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