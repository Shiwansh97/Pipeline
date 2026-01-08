import pandas as pd
import streamlit as st
from db import get_engine

engine = get_engine()

st.set_page_config(page_title="PostgreSQL Dashboard", layout="wide")
st.title("📊 PostgreSQL Ingestion Dashboard")

tables = pd.read_sql("""
    SELECT tablename
    FROM pg_tables
    WHERE schemaname = 'public'
    ORDER BY tablename DESC
""", engine)

table_name = st.selectbox("Select Table", tables["tablename"])

df = pd.read_sql(f"SELECT * FROM {table_name}", engine)

st.metric("Total Records", len(df))
st.dataframe(df)

if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"])
    # st.line_chart(df.groupby(df["created_at"].dt.date).size())
    st.bar_chart(df.groupby(df["created_at"].dt.date).size())
if "status" in df.columns:
    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)
    # st.pie_chart(status_counts)
import plotly.express as px

columns = df.columns.tolist()
selected_col = st.selectbox("Select column for Pie Chart", columns)

fig = px.pie(df, names=selected_col, title=f"{selected_col} Distribution")
st.plotly_chart(fig, use_container_width=True)
