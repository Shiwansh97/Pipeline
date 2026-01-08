import os
import pandas as pd
from datetime import datetime
from db import get_engine

engine = get_engine()

def read_file(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Only CSV and Excel files are supported")

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

def generate_table_name(file_path: str) -> str:
    base = os.path.splitext(os.path.basename(file_path))[0]
    base = base.lower().replace(" ", "_").replace("-", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}"

def load_to_postgres(df: pd.DataFrame, table_name: str):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="fail",   # 🔥 new table every run
        index=False
    )

def run_pipeline(file_path: str):
    print("📥 Reading file...")
    df = read_file(file_path)
    print(f"   - Read {len(df)} records.")
    print("🧹 Cleaning columns...")
    df = clean_columns(df)

    table_name = generate_table_name(file_path)
    print(f"🗄️ Creating table: {table_name}")

    load_to_postgres(df, table_name)

    print("✅ Pipeline completed successfully")


if __name__ == "__main__":
    FILE_PATH = r"D:\Pipeline\data\source_dir\Churn_Modelling (1) (1).csv"
    TABLE_NAME = "sample_data"

    run_pipeline(FILE_PATH, TABLE_NAME)
