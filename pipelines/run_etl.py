from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

from pipelines.ingest.defillama_market import (
    fetch_total_defi_tvl_chart,
    fetch_protocols_snapshot,
    fetch_categories_snapshot,  
)

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"
MARTS = WAREHOUSE / "marts"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs():
    MARTS.mkdir(parents=True, exist_ok=True)


def write_parquet(df: pd.DataFrame, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)


def main():
    ensure_dirs()
    refresh_ts = now_utc_iso()

    tvl = fetch_total_defi_tvl_chart()
    if tvl is None or tvl.empty:
        tvl = pd.DataFrame(columns=["ts_utc", "tvl_usd", "source"])

    prot = fetch_protocols_snapshot(top_n=20)
    if prot is None or prot.empty:
        prot = pd.DataFrame(columns=[
            "name", "slug", "category", "chain",
            "tvl_usd", "change_1d_pct", "change_7d_pct", "change_1m_pct",
            "ts_utc", "source"
        ])

    cats_api = fetch_categories_snapshot()
    if cats_api is None:
        cats_api = pd.DataFrame(columns=["category", "tvl_usd", "ts_utc", "source"])

    if not prot.empty and "category" in prot.columns and "tvl_usd" in prot.columns:
        cats = prot.copy()
        cats["category"] = cats["category"].fillna("Unknown")
        cats["tvl_usd"] = pd.to_numeric(cats["tvl_usd"], errors="coerce").fillna(0.0)
        cats = (
            cats.groupby("category", as_index=False)["tvl_usd"]
            .sum()
            .sort_values("tvl_usd", ascending=False)
        )
        cats["ts_utc"] = refresh_ts
        cats["source"] = "defillama_protocols_agg"
    else:
        cats = cats_api  

    meta = pd.DataFrame([{
        "ts_utc": refresh_ts,
        "pipeline": "defillama_macro",
        "status": "ok",
        "notes": "Total TVL + top protocols + categories (protocols-agg fallback)",
    }])

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
    main()
