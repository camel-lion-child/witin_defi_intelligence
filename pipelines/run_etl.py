"""This script runs a DeFiLlama ETL pipeline to build analytical marts for total TVL, 
top protocols, protocol categories, and refresh metadata.

Ce script exécute un pipeline ETL DeFiLlama afin de construire des marts analytiques pour la TVL totale, 
les principaux protocoles, les catégories de protocoles et les métadonnées de rafraîchissement."""

from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

from pipelines.ingest.defillama_market import (
    fetch_total_defi_tvl_chart,
    fetch_protocols_snapshot,
    fetch_categories_snapshot,  
)
#define project path
ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"
MARTS = WAREHOUSE / "marts"

#return current UTC timestamp in ISO format
def now_utc_iso() -> str: 
    return datetime.now(timezone.utc).isoformat()

#ensure mart/output directory exists
def ensure_dirs():
    MARTS.mkdir(parents=True, exist_ok=True)

#save dataframe as parquet file
def write_parquet(df: pd.DataFrame, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)


def main():
    ensure_dirs() #prepare output folders & refresh timestamp
    refresh_ts = now_utc_iso()

    tvl = fetch_total_defi_tvl_chart() #fetch total DeFi TVL (total value locked) time series
    if tvl is None or tvl.empty:
        tvl = pd.DataFrame(columns=["ts_utc", "tvl_usd", "source"])

    prot = fetch_protocols_snapshot(top_n=20) #fetch top protocol snapshot
    if prot is None or prot.empty:
        prot = pd.DataFrame(columns=[
            "name", "slug", "category", "chain",
            "tvl_usd", "change_1d_pct", "change_7d_pct", "change_1m_pct",
            "ts_utc", "source"
        ])

    cats_api = fetch_categories_snapshot() #fetch categories snapshot directly from API
    if cats_api is None:
        cats_api = pd.DataFrame(columns=["category", "tvl_usd", "ts_utc", "source"])
    #build category aggregation from protocol-level data when available
    if not prot.empty and "category" in prot.columns and "tvl_usd" in prot.columns:
        cats = prot.copy()
        cats["category"] = cats["category"].fillna("Unknown")
        cats["tvl_usd"] = pd.to_numeric(cats["tvl_usd"], errors="coerce").fillna(0.0)
        #aggregate TVL by protocol category
        cats = (
            cats.groupby("category", as_index=False)["tvl_usd"]
            .sum()
            .sort_values("tvl_usd", ascending=False)
        )
        cats["ts_utc"] = refresh_ts #add refresh metadata
        cats["source"] = "defillama_protocols_agg"
    else:
        cats = cats_api  #fall back to API provided category snapshot if protocol data in unavailable
    
    #store ETL run metadata for monitoring / traceability 
    meta = pd.DataFrame([{
        "ts_utc": refresh_ts,
        "pipeline": "defillama_macro",
        "status": "ok",
        "notes": "Total TVL + top protocols + categories (protocols-agg fallback)",
    }])

    #save mart / analytical outputs
    write_parquet(tvl, MARTS / "fact_defi_tvl.parquet")
    write_parquet(prot, MARTS / "dim_protocols_top.parquet")
    write_parquet(cats, MARTS / "dim_categories.parquet")
    write_parquet(meta, MARTS / "meta_refresh.parquet")

    print("ETL done")
    print(f"- {MARTS / 'fact_defi_tvl.parquet'}")
    print(f"- {MARTS / 'dim_protocols_top.parquet'}")
    print(f"- {MARTS / 'dim_categories.parquet'}")
    print(f"- {MARTS / 'meta_refresh.parquet'}")


if __name__ == "__main__":
    main() #entry point: run Defillama ETL & generate analytical marts
