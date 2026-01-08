import os
import pandas as pd
from db import get_engine

engine = get_engine()

def read_file(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Only CSV and Excel files are supported")

    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def load_to_postgres(df: pd.DataFrame, table_name: str):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",   # auto-creates table if not exists
        index=False,
        chunksize=5000,
        method="multi"
    )


def run_pipeline(file_path: str, table_name: str):
    print("📥 Reading file...")
    df = read_file(file_path)

    print("🧹 Cleaning column names...")
    df = clean_columns(df)

    print("🗄️ Loading data into PostgreSQL...")
    load_to_postgres(df, table_name)

    print("✅ Pipeline completed successfully")


if __name__ == "__main__":
    FILE_PATH = "data/sample.csv"   # change file here
    TABLE_NAME = "sample_data"      # postgres table name

    run_pipeline(FILE_PATH, TABLE_NAME)
