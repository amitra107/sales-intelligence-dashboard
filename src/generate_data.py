import numpy as np
import pandas as pd

np.random.seed(42)

n = 10000

products = {
    "Laptop": ("Electronics", 650, 1400),
    "Monitor": ("Electronics", 150, 500),
    "Keyboard": ("Accessories", 30, 150),
    "Mouse": ("Accessories", 15, 100),
    "Headphones": ("Accessories", 40, 250),
    "Office Chair": ("Furniture", 120, 500),
    "Desk": ("Furniture", 100, 600),
    "Printer": ("Electronics", 100, 450),
    "Tablet": ("Electronics", 200, 900),
    "Webcam": ("Accessories", 40, 200),
}

regions = ["North", "South", "East", "West"]
customers = [f"CUST-{i:04d}" for i in range(1, 1001)]

product_names = np.random.choice(list(products.keys()), n)

data = []

for i in range(n):
    product = product_names[i]
    category, min_price, max_price = products[product]

    quantity = np.random.randint(1, 6)
    unit_price = round(np.random.uniform(min_price, max_price), 2)
    discount = round(np.random.choice(
        [0, 0.05, 0.10, 0.15, 0.20],
        p=[0.35, 0.20, 0.25, 0.15, 0.05]
    ), 2)

    sales = round(quantity * unit_price * (1 - discount), 2)

    cost_rate = np.random.uniform(0.55, 0.82)
    cost = round(sales * cost_rate, 2)
    profit = round(sales - cost, 2)

    data.append({
        "Order_ID": f"ORD-{i+1:05d}",
        "Order_Date": pd.Timestamp("2025-01-01") +
                      pd.Timedelta(days=np.random.randint(0, 365)),
        "Customer_ID": np.random.choice(customers),
        "Product": product,
        "Category": category,
        "Region": np.random.choice(regions),
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Cost": cost,
        "Profit": profit,
    })

df = pd.DataFrame(data)

df.to_csv("data/raw/sales_data.csv", index=False)

print(f"Dataset created successfully: {len(df):,} rows")
print(f"Saved to: data/raw/sales_data.csv")
print("\nColumns:")
print(df.columns.tolist())