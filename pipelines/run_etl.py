from pathlib import Path
from pipelines.ingest.binance_prices import fetch_prices_usdt
from pipelines.ingest.defillama_aave import fetch_aave_protocol_snapshot
from pipelines.transform.marts import (
    build_dim_prices,
    build_fact_protocol_snapshot,
    build_fact_risk_placeholder,
)
from pipelines.utils.io import write_parquet, replace_table

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"
DB_PATH = WAREHOUSE / "witin.duckdb"

def main():
    # INGEST
    raw_prices = fetch_prices_usdt()
    raw_aave = fetch_aave_protocol_snapshot()

    write_parquet(raw_prices, WAREHOUSE / "raw" / "binance_prices.parquet")
    write_parquet(raw_aave, WAREHOUSE / "raw" / "aave_protocol_snapshot.parquet")

    # TRANSFORM
    dim_prices = build_dim_prices(raw_prices)
    fact_protocol = build_fact_protocol_snapshot(raw_aave)
    fact_risk = build_fact_risk_placeholder(dim_prices)

    write_parquet(dim_prices, WAREHOUSE / "marts" / "dim_prices.parquet")
    write_parquet(fact_protocol, WAREHOUSE / "marts" / "fact_protocol_snapshot.parquet")
    write_parquet(fact_risk, WAREHOUSE / "marts" / "fact_risk_scenarios.parquet")

    # LOAD (DuckDB)
    replace_table(dim_prices, DB_PATH, "dim_prices")
    replace_table(fact_protocol, DB_PATH, "fact_protocol_snapshot")
    replace_table(fact_risk, DB_PATH, "fact_risk_scenarios")

    print("ETL OK")
    print(f"DuckDB: {DB_PATH}")

if __name__ == "__main__":
    main()
