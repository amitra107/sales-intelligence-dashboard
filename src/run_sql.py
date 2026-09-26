import os
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE = "sqlite:///data/sales.db"
OUTPUT_DIR = "reports"

engine = create_engine(DATABASE)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_query(query, output_file):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    output_path = os.path.join(OUTPUT_DIR, output_file)
    df.to_csv(output_path, index=False)

    print(f"Created: {output_path}")
    print(f"Rows: {len(df)}")


queries = {
    "sales_by_region.csv": """
        SELECT
            Region,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            COUNT(DISTINCT Order_ID) AS total_orders
        FROM sales
        GROUP BY Region
        ORDER BY total_sales DESC;
    """,

    "sales_by_category.csv": """
        SELECT
            Category,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit
        FROM sales
        GROUP BY Category
        ORDER BY total_sales DESC;
    """,

    "top_products.csv": """
        SELECT
            Product,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            SUM(Quantity) AS units_sold
        FROM sales
        GROUP BY Product
        ORDER BY total_sales DESC
        LIMIT 10;
    """,

    "top_customers.csv": """
        SELECT
            Customer_ID,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            COUNT(DISTINCT Order_ID) AS total_orders
        FROM sales
        GROUP BY Customer_ID
        ORDER BY total_sales DESC
        LIMIT 10;
    """,

    "monthly_performance.csv": """
        SELECT
            Year,
            Month,
            Month_Name,
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            COUNT(DISTINCT Order_ID) AS total_orders
        FROM sales
        GROUP BY Year, Month, Month_Name
        ORDER BY Year, Month;
    """
}


for output_file, query in queries.items():
    run_query(query, output_file)

print("\nSQL analysis completed successfully.")