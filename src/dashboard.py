import pandas as pd
import streamlit as st
from db import get_engine

engine = get_engine()

st.set_page_config(page_title="Postgres Dashboard", layout="wide")
st.title("📊 PostgreSQL Data Dashboard")

df = pd.read_sql("SELECT * FROM sample_data", engine)

st.metric("Total Records", len(df))
st.dataframe(df)

if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"])
    st.line_chart(df.groupby(df["created_at"].dt.date).size())
