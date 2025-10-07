import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Price Tracker Dashboard", layout="wide")

conn = sqlite3.connect("data/prices.db")
df = pd.read_sql_query("SELECT * FROM prices ORDER BY scraped_at DESC", conn)

st.title("📊 Price Tracker Dashboard")
st.write("Auto-refreshes with each scrape run!")

st.dataframe(df.head(50))

avg_price = df.groupby("source")["price"].mean().reset_index()
st.bar_chart(avg_price, x="source", y="price")

if st.button("Refresh Data"):
    st.experimental_rerun()
