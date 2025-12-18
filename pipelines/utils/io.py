from pathlib import Path
from typing import Union
import pandas as pd
import duckdb

def ensure_dir(path: Union[str, Path]) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_parquet(df: pd.DataFrame, path: Union[str, Path]) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    df.to_parquet(path, index=False)

def replace_table(df: pd.DataFrame, db_path: Union[str, Path], table: str) -> None:
    db_path = Path(db_path)
    ensure_dir(db_path.parent)
    con = duckdb.connect(str(db_path))
    con.register("df_view", df)
    con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df_view LIMIT 0")
    con.execute(f"DELETE FROM {table}")
    con.execute(f"INSERT INTO {table} SELECT * FROM df_view")
    con.close()

