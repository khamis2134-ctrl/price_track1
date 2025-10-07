"""
run_dashboard.py
Simple Streamlit dashboard to inspect latest prices.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from app.db import Database

ROOT = Path(__file__).parent.resolve()
DB_FILE = ROOT / "data" / "prices.db"

def load_data(limit=1000):
    db = Database(DB_FILE)
    db.init_db()
    rows = db.fetch_all_prices(limit=limit)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)

def main():
    st.set_page_config(page_title="PriceTrack Dashboard", layout="wide")
    st.title("PriceTrack — Dashboard")
    df = load_data(1000)
    if df.empty:
        st.info("No price data available. Run main.py --once to populate sample data.")
        return

    srcs = st.multiselect("Source", options=sorted(df["source"].unique()), default=sorted(df["source"].unique()))
    df = df[df["source"].isin(srcs)]
    product = st.selectbox("Product (id)", options=["All"] + sorted(df["product_id"].astype(str).unique().tolist()))
    if product != "All":
        df = df[df["product_id"].astype(str) == product]
    st.dataframe(df.head(200))

    # simple chart
    if not df.empty:
        df['scraped_at'] = pd.to_datetime(df['scraped_at'])
        df = df.sort_values("scraped_at")
        chart_df = df.groupby("scraped_at").agg({"price_value": "mean"}).reset_index()
        st.line_chart(chart_df.rename(columns={"scraped_at": "index"}).set_index("index")["price_value"])

if __name__ == "__main__":
    main()
