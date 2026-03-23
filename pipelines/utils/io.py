"""This utility module provides reusable helpers to create directories, save parquet files, 
and fully refresh DuckDB tables from pandas DataFrames.

Ce module utilitaire fournit des fonctions réutilisables pour créer des dossiers, sauvegarder des fichiers parquet 
et remplacer complètement des tables DuckDB à partir de DataFrames pandas."""


from pathlib import Path
from typing import Union
import pandas as pd
import duckdb

def ensure_dir(path: Union[str, Path]) -> Path: #ensure a directory exists before writing files
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_parquet(df: pd.DataFrame, path: Union[str, Path]) -> None: #save dataframe as parquet, create parent if needed
    path = Path(path)
    ensure_dir(path.parent)
    df.to_parquet(path, index=False)

def replace_table(df: pd.DataFrame, db_path: Union[str, Path], table: str) -> None: #replace all data in duckdb table with a new dataframe
    db_path = Path(db_path)
    ensure_dir(db_path.parent)
    con = duckdb.connect(str(db_path)) #connect to duckdb database
    con.register("df_view", df) #register dataframe as temporary view
    con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df_view LIMIT 0") #create table with same schema if it doesn't exist
    con.execute(f"DELETE FROM {table}") #remove existing rows
    con.execute(f"INSERT INTO {table} SELECT * FROM df_view") #insert fresh data
    con.close() #close database connection

