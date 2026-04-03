"""This module provides reusable DeFiLlama ingestion functions to fetch total TVL, protocol snapshots, and category snapshots, 
while handling unstable API payloads defensively.

Ce module fournit des fonctions réutilisables d’ingestion DeFiLlama pour récupérer la TVL totale, 
les snapshots de protocoles et les snapshots de catégories, tout en gérant de manière robuste les variations de payload de l’API."""

import requests
import pandas as pd
from datetime import datetime, timezone
from typing import Any, Optional

BASE = "https://api.llama.fi" #base URL for Defillama API


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat() #return current UTC timestamp in ISO format


def _get_json(url: str, params: Optional[dict] = None, timeout: int = 30) -> Any:
    r = requests.get(url, params=params, timeout=timeout) #genetic helper to call API endpoint & return json
    if r.status_code == 404:
        return None #return None instead of failing if endpoint doesn't exist
    r.raise_for_status() #raise exeption for other HTTP errors
    return r.json()


def _to_float(v): #safely convert a value to float
    try:
        return float(v) if v is not None else None
    except Exception:
        return None


def fetch_total_defi_tvl_chart() -> pd.DataFrame:
    """
    GET /charts
    Output: ts_utc, tvl_usd, source
    """
    data = _get_json(f"{BASE}/charts")
    #return empty dataframe if response is missing on invalid
    if data is None or not isinstance(data, list):
        return pd.DataFrame(columns=["ts_utc", "tvl_usd", "source"])

    rows = []
    for x in data:
        if not isinstance(x, dict):
            continue
        dt = x.get("date")
        tvl = x.get("totalLiquidityUSD")
        if dt is None or tvl is None: #skip incomplete observations
            continue
        tvl_f = _to_float(tvl)
        if tvl_f is None:
            continue
        try: #convert unix timestamp safely
            dt_i = int(dt)
        except Exception:
            continue
        rows.append(
            {"ts_utc": pd.to_datetime(dt_i, unit="s", utc=True), "tvl_usd": tvl_f, "source": "defillama"}
        )

    df = pd.DataFrame(rows)
    if df.empty: #return empty schema if no valid rows were parsed
        return pd.DataFrame(columns=["ts_utc", "tvl_usd", "source"])
    return df.sort_values("ts_utc").reset_index(drop=True)


def fetch_protocols_snapshot(top_n: int = 20) -> pd.DataFrame:
    """
    GET /protocols
    Output: name, slug, category, chain, tvl_usd, change_1d_pct, change_7d_pct, change_1m_pct, ts_utc, source
    """
    data = _get_json(f"{BASE}/protocols")
    cols = [
        "name", "slug", "category", "chain",
        "tvl_usd", "change_1d_pct", "change_7d_pct", "change_1m_pct",
        "ts_utc", "source"
    ]
    if data is None or not isinstance(data, list):
        return pd.DataFrame(columns=cols)

    ts = _now_utc_iso()
    rows = []
    for x in data:
        if not isinstance(x, dict):
            continue

        name = x.get("name")
        slug = x.get("slug")
        if not name or not slug:
            continue

        rows.append({
            "name": name,
            "slug": slug,
            "category": x.get("category"),
            "chain": x.get("chain"),
            "tvl_usd": _to_float(x.get("tvl")) or 0.0,
            "change_1d_pct": _to_float(x.get("change_1d")),
            "change_7d_pct": _to_float(x.get("change_7d")),
            "change_1m_pct": _to_float(x.get("change_1m")),
            "ts_utc": ts,
            "source": "defillama",
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=cols)

    df["tvl_usd"] = pd.to_numeric(df["tvl_usd"], errors="coerce").fillna(0.0)
    df = df.sort_values("tvl_usd", ascending=False).head(top_n).reset_index(drop=True)
    return df


def fetch_categories_snapshot() -> pd.DataFrame:
    """
    GET /categories (payload changes a lot).
    We keep it defensive and optional.
    Output: category, tvl_usd, ts_utc, source
    """
    data = _get_json(f"{BASE}/categories")
    cols = ["category", "tvl_usd", "ts_utc", "source"]
    ts = _now_utc_iso()

    if data is None:
        return pd.DataFrame(columns=cols)

    rows = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                cat = item.get("name") or item.get("category")
                if not cat:
                    continue
                tvl = _to_float(item.get("tvl")) or 0.0
                rows.append({"category": str(cat), "tvl_usd": tvl, "ts_utc": ts, "source": "defillama"})
            elif isinstance(item, str):
                # names-only
                rows.append({"category": item, "tvl_usd": 0.0, "ts_utc": ts, "source": "defillama"})

    elif isinstance(data, dict):
        maybe = data.get("categories") or data.get("data") or data.get("items") or []
        if isinstance(maybe, list):
            for item in maybe:
                if not isinstance(item, dict):
                    continue
                cat = item.get("name") or item.get("category")
                if not cat:
                    continue
                tvl = _to_float(item.get("tvl")) or 0.0
                rows.append({"category": str(cat), "tvl_usd": tvl, "ts_utc": ts, "source": "defillama"})

    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=cols)

    df["tvl_usd"] = pd.to_numeric(df["tvl_usd"], errors="coerce").fillna(0.0)
    return df.sort_values("tvl_usd", ascending=False).reset_index(drop=True)

