import streamlit as st
import pandas as pd
from pathlib import Path
from app.layout import setup_page
from app.styles import card

setup_page("Dashboards — WITIN")

ROOT = Path(__file__).resolve().parents[2]
MARTS = ROOT / "warehouse" / "marts"

TVL_FP = MARTS / "fact_defi_tvl.parquet"
CATS_FP = MARTS / "dim_categories.parquet"
PROT_FP = MARTS / "dim_protocols_top.parquet"

def _read(fp: Path) -> pd.DataFrame:
    return pd.read_parquet(fp) if fp.exists() else pd.DataFrame()

def _pct_change(series: pd.Series, periods: int) -> float:
    if series is None or len(series) < periods + 1:
        return 0.0
    latest = float(series.iloc[-1])
    prev = float(series.iloc[-(periods + 1)])
    if prev == 0:
        return 0.0
    return (latest / prev - 1.0) * 100.0

st.title("Dashboards")
st.caption("Macro-first dashboards (DefiLlama-style): TVL, categories, and protocol landscape.")

tvl = _read(TVL_FP)
cats = _read(CATS_FP)
prot = _read(PROT_FP)

if tvl.empty:
    st.warning("Missing marts. Run ETL first: `python -m pipelines.run_etl`")
    st.stop()

tvl["ts_utc"] = pd.to_datetime(tvl["ts_utc"], utc=True, errors="coerce")
tvl = tvl.dropna(subset=["ts_utc"]).sort_values("ts_utc")

latest_tvl = float(tvl["tvl_usd"].iloc[-1])
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
    cats["tvl_usd"] = pd.to_numeric(cats["tvl_usd"], errors="coerce").fillna(0.0)
    cats = cats.sort_values("tvl_usd", ascending=False).head(12)
    st.bar_chart(cats.set_index("category")["tvl_usd"])
    st.dataframe(cats, use_container_width=True, hide_index=True)

st.divider()

st.markdown("## Protocol landscape (Top 20)")
if prot.empty:
    st.info("Protocol snapshot not available yet.")
else:
    prot["tvl_usd"] = pd.to_numeric(prot["tvl_usd"], errors="coerce").fillna(0.0)
    prot = prot.sort_values("tvl_usd", ascending=False)
    st.dataframe(
        prot[["name","category","chain","tvl_usd","change_1d_pct","change_7d_pct","change_1m_pct"]],
        use_container_width=True,
        hide_index=True,
    )
