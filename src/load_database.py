import pandas as pd
from sqlalchemy import create_engine

INPUT_FILE = "data/processed/sales_clean.csv"
DATABASE = "sqlite:///data/sales.db"

df = pd.read_csv(INPUT_FILE)

engine = create_engine(DATABASE)

df.to_sql(
    "sales",
    engine,
    if_exists="replace",
    index=False
)

print(f"Loaded {len(df):,} rows into the sales table.")
print("Database: data/sales.db")