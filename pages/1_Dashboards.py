"""I build a Streamlit dashboard on top of my data pipeline to monitor market size, capital flows, and protocol activity in real time.

Je construis un dashboard Streamlit basé sur mon pipeline de données pour suivre la taille du marché, 
les flux de capital et l’activité des protocoles en temps réel."""

from typing import Optional
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd

from layout import setup_page
from styles import card


setup_page("Dashboards — WITIN")

MARTS = ROOT / "warehouse" / "marts"

TVL_FP = MARTS / "fact_defi_tvl.parquet"
CATS_FP = MARTS / "dim_categories.parquet"
PROT_FP = MARTS / "dim_protocols_top.parquet"


def _read(fp: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(fp) if fp.exists() else pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to read {fp.name}: {e}")
        return pd.DataFrame()


def _pct_change(series: pd.Series, periods: int) -> float:
    if series is None or len(series) < periods + 1:
        return 0.0
    latest = float(series.iloc[-1])
    prev = float(series.iloc[-(periods + 1)])
    if prev == 0:
        return 0.0
    return (latest / prev - 1.0) * 100.0


def _pick_ts_column(df: pd.DataFrame) -> Optional[str]:
    candidates = [
        "ts_utc",
        "timestamp",
        "ts",
        "datetime",
        "date",
        "dt",
        "block_time",
        "time",
    ]
    for c in candidates:
        if c in df.columns:
            return c
    lowered = {c: str(c).lower() for c in df.columns}
    for c, lc in lowered.items():
        if ("ts" in lc) or ("time" in lc) or ("date" in lc):
            return c
    return None


st.title("Dashboards")
st.caption("Macro-first dashboards (DefiLlama-style): TVL, categories, and protocol landscape.")

tvl = _read(TVL_FP)
cats = _read(CATS_FP)
prot = _read(PROT_FP)

if tvl.empty:
    st.warning("Missing marts. Run ETL first:\n\n`python3 -m pipelines.run_etl`")
    st.info(f"Expected file at: {TVL_FP}")
    st.stop()

ts_col = _pick_ts_column(tvl)
if ts_col is None:
    st.error(f"Could not find a timestamp column in TVL mart. Columns: {list(tvl.columns)}")
    st.stop()

tvl["ts_utc"] = pd.to_datetime(tvl[ts_col], utc=True, errors="coerce")

if "tvl_usd" not in tvl.columns:
    fallbacks = ["tvl", "tvlUsd", "tvl_usd_value", "total_tvl_usd", "tvlUSD"]
    tvl_col = next((c for c in fallbacks if c in tvl.columns), None)
    if tvl_col is None:
        st.error(f"Could not find TVL value column. Columns: {list(tvl.columns)}")
        st.stop()
    tvl["tvl_usd"] = pd.to_numeric(tvl[tvl_col], errors="coerce")
else:
    tvl["tvl_usd"] = pd.to_numeric(tvl["tvl_usd"], errors="coerce")

tvl = tvl.dropna(subset=["ts_utc", "tvl_usd"]).sort_values("ts_utc")

latest_tvl = float(tvl["tvl_usd"].iloc[-1]) if len(tvl) else 0.0
tvl_7d = _pct_change(tvl["tvl_usd"], 7)

k1, k2, k3 = st.columns(3)
with k1:
    card("Total DeFi TVL", f"{latest_tvl:,.0f} USD", "Market-wide capital deployed in DeFi")
with k2:
    card("TVL change (7D)", f"{tvl_7d:,.2f}%", "Short-term expansion / contraction")
with k3:
    card("Data sources", "DefiLlama", "Free public endpoints")

st.divider()

st.markdown("## DeFi TVL trend")
st.line_chart(tvl.set_index("ts_utc")["tvl_usd"])

st.divider()

st.markdown("## TVL by category")
if cats.empty:
    st.info("Category snapshot not available yet.")
else:
    if "category" not in cats.columns:
        cat_col = next((c for c in ["name", "cat", "sector"] if c in cats.columns), None)
        if cat_col:
            cats["category"] = cats[cat_col]
        else:
            st.error(f"Category column not found. Columns: {list(cats.columns)}")
            st.stop()

    if "tvl_usd" not in cats.columns:
        tvl_cat_col = next((c for c in ["tvl", "tvlUSD", "tvlUsd"] if c in cats.columns), None)
        if tvl_cat_col:
            cats["tvl_usd"] = cats[tvl_cat_col]
        else:
            st.error(f"Category TVL column not found. Columns: {list(cats.columns)}")
            st.stop()

    cats["tvl_usd"] = pd.to_numeric(cats["tvl_usd"], errors="coerce").fillna(0.0)
    cats = cats.sort_values("tvl_usd", ascending=False).head(12)

    st.bar_chart(cats.set_index("category")["tvl_usd"])
    st.dataframe(cats, use_container_width=True, hide_index=True)

st.divider()

st.markdown("## Protocol landscape (Top 20)")
if prot.empty:
    st.info("Protocol snapshot not available yet.")
else:
    if "tvl_usd" not in prot.columns:
        tvl_p_col = next((c for c in ["tvl", "tvlUSD", "tvlUsd"] if c in prot.columns), None)
        if tvl_p_col:
            prot["tvl_usd"] = prot[tvl_p_col]
        else:
            st.error(f"Protocol TVL column not found. Columns: {list(prot.columns)}")
            st.stop()

    prot["tvl_usd"] = pd.to_numeric(prot["tvl_usd"], errors="coerce").fillna(0.0)
    prot = prot.sort_values("tvl_usd", ascending=False)

    for col in ["name", "category", "chain", "change_1d_pct", "change_7d_pct", "change_1m_pct"]:
        if col not in prot.columns:
            prot[col] = None

    st.dataframe(
        prot[["name", "category", "chain", "tvl_usd", "change_1d_pct", "change_7d_pct", "change_1m_pct"]].head(20),
        use_container_width=True,
        hide_index=True,
    )
