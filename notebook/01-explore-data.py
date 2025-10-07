# A simple script-style notebook for exploring the DB. Save as .py or copy into Jupyter.
import pandas as pd
from app.db import fetch_all
from config.env_loader import load_env

env = load_env('dev')
rows = fetch_all(env)
df = pd.DataFrame(rows)
print(df.head())

# Basic stats
print('Count:', len(df))
print(df.groupby('product_name')['price'].agg(['min','max','mean']).sort_values('mean', ascending=False).head(10))

# Save CSV for Looker Studio
Path('data').mkdir(exist_ok=True)
df.to_csv('data/latest_prices.csv', index=False)
