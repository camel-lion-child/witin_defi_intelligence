import requests
import pandas as pd
from datetime import datetime, timezone

def fetch_aave_protocol_snapshot() -> pd.DataFrame:
    url = "https://api.llama.fi/protocol/aave"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()

    ts = datetime.now(timezone.utc).isoformat()
    return pd.DataFrame([{
        "protocol": data.get("name", "Aave"),
        "tvl_usd": data.get("tvl"),
        "category": data.get("category"),
        "ts_utc": ts,
    }])