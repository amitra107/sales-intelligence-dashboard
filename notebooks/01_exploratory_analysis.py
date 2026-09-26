import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("data/processed/sales_clean.csv")

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate orders:")
print(df["Order_ID"].duplicated().sum())

# -----------------------------
# KPI calculations
# -----------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()
average_order_value = total_sales / total_orders
profit_margin = total_profit / total_sales

print("\n========== BUSINESS KPIs ==========")
print(f"Total Sales: ₹{total_sales:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Units Sold: {total_units:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Profit Margin: {profit_margin:.2%}")

# -----------------------------
# Sales by region
# -----------------------------

region_sales = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Sales", ascending=False)
)

print("\n========== SALES BY REGION ==========")
print(region_sales)

# -----------------------------
# Sales by category
# -----------------------------

category_sales = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
)

print("\n========== SALES BY CATEGORY ==========")
print(category_sales)

# -----------------------------
# Product performance
# -----------------------------

product_sales = (
    df.groupby("Product")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
)

print("\n========== PRODUCT PERFORMANCE ==========")
print(product_sales)

# -----------------------------
# Monthly performance
# -----------------------------

monthly_sales = (
    df.groupby(["Year", "Month", "Month_Name"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .reset_index()
    .sort_values(["Year", "Month"])
)

print("\n========== MONTHLY PERFORMANCE ==========")
print(monthly_sales)