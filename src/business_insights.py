import pandas as pd

df = pd.read_csv("data/processed/sales_clean.csv")

print("\n========== BUSINESS INSIGHTS ==========\n")

# Overall KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
profit_margin = total_profit / total_sales * 100

print(f"Total Sales: ₹{total_sales:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Profit Margin: {profit_margin:.2f}%")

# Region
region = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Sales", ascending=False)
)

print("\n--- Regional Performance ---")
print(region)

# Category
category = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Sales", ascending=False)
)

print("\n--- Category Performance ---")
print(category)

# Products
products = (
    df.groupby("Product")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum")
    )
)

print("\n--- Top Products by Sales ---")
print(products.sort_values("Sales", ascending=False).head(10))

print("\n--- Top Products by Profit ---")
print(products.sort_values("Profit", ascending=False).head(10))

# Customers
customers = (
    df.groupby("Customer_ID")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
)

print("\n--- Top Customers by Sales ---")
print(customers.sort_values("Sales", ascending=False).head(10))

# Monthly
monthly = (
    df.assign(Month=df["Order_Date"].str[:7])
    .groupby("Month")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

print("\n--- Monthly Performance ---")
print(monthly)