import pandas as pd

INPUT_FILE = "data/raw/sales_data.csv"
OUTPUT_FILE = "data/processed/sales_clean.csv"


def clean_sales_data():
    df = pd.read_csv(INPUT_FILE)

    print("Original shape:", df.shape)

    # Convert date
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["Order_ID"])

    # Remove rows with missing critical values
    critical_columns = [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product",
        "Category",
        "Region",
        "Sales",
        "Profit",
    ]

    df = df.dropna(subset=critical_columns)

    # Ensure numeric columns are numeric
    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Discount",
        "Sales",
        "Cost",
        "Profit",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove invalid transactions
    df = df[
        (df["Quantity"] > 0)
        & (df["Unit_Price"] > 0)
        & (df["Sales"] >= 0)
        & (df["Cost"] >= 0)
    ]

    # Add analytical columns
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.month_name()
    df["Profit_Margin"] = (df["Profit"] / df["Sales"]).round(4)

    # Create processed directory
    import os
    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Cleaned shape:", df.shape)
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_sales_data()