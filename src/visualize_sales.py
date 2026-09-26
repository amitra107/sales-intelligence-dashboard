import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("data/processed/sales_clean.csv")

os.makedirs("reports/charts", exist_ok=True)

# -----------------------------
# Monthly sales trend
# -----------------------------

monthly = (
    df.groupby(["Year", "Month"])
    .agg(Sales=("Sales", "sum"))
    .reset_index()
)

monthly["Period"] = (
    monthly["Year"].astype(str)
    + "-"
    + monthly["Month"].astype(str).str.zfill(2)
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly,
    x="Period",
    y="Sales",
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/charts/monthly_sales_trend.png",
    dpi=300
)

plt.close()

# -----------------------------
# Regional sales
# -----------------------------

region = (
    df.groupby("Region")
    .agg(Sales=("Sales", "sum"))
    .reset_index()
    .sort_values("Sales", ascending=False)
)

plt.figure(figsize=(8, 5))

sns.barplot(
    data=region,
    x="Region",
    y="Sales"
)

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "reports/charts/sales_by_region.png",
    dpi=300
)

plt.close()

print("Charts created successfully.")