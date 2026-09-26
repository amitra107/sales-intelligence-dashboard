import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    [data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 15px;
        border-radius: 10px;
    }

    [data-testid="stMetricLabel"] {
        color: #d1d5db;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    h1 {
        font-size: 2.2rem;
    }

    h2, h3 {
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)
# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/sales_clean.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("Sales Intelligence Dashboard")
st.caption("Interactive sales, revenue and profitability analysis")
st.info(
    "Use the filters in the sidebar to explore sales performance "
    "across different regions, categories and time periods."
)
# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Add this here
st.sidebar.divider()

st.sidebar.caption(
    "Dashboard updates automatically when filters change."
)

# Then continue with the filtering
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories)) &
        (df["Order_Date"].dt.date >= start_date) &
        (df["Order_Date"].dt.date <= end_date)
    ]
else:
    filtered_df = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories))
    ]
# -----------------------------
# KPI calculations
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_units = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

average_order_value = (
    total_sales / total_orders
    if total_orders != 0 else 0
)

# -----------------------------
# KPI cards
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)

col5.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)
# -----------------------------
# Monthly performance
# -----------------------------
monthly = (
    filtered_df
    .groupby(filtered_df["Order_Date"].dt.to_period("M"))
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly["Order_Date"] = monthly["Order_Date"].astype(str)

fig_monthly = px.line(
    monthly,
    x="Order_Date",
    y=["Sales", "Profit"],
    markers=True,
    title="Monthly Sales & Profit"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------------
# Region and Category
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    region_data = (
        filtered_df
        .groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_region = px.bar(
        region_data,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    category_data = (
        filtered_df
        .groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_data,
        x="Category",
        y="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(fig_category, use_container_width=True)

# -----------------------------
# Product Performance
# -----------------------------
st.subheader("Product Performance")

product_data = (
    filtered_df
    .groupby("Product", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    fig_products = px.bar(
        product_data.head(10),
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Sales"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

with col2:
    profit_products = product_data.sort_values(
        "Profit",
        ascending=False
    ).head(10)

    fig_profit = px.bar(
        profit_products,
        x="Profit",
        y="Product",
        orientation="h",
        title="Top 10 Products by Profit"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )
# -----------------------------
# Customer Performance
# -----------------------------
st.subheader("Customer Performance")

customer_data = (
    filtered_df
    .groupby("Customer_ID", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Sales", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    top_customers = customer_data.head(10)

    fig_customers = px.bar(
        top_customers,
        x="Sales",
        y="Customer_ID",
        orientation="h",
        title="Top 10 Customers by Revenue"
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )

with col2:
    top_profit_customers = (
        customer_data
        .sort_values("Profit", ascending=False)
        .head(10)
    )

    fig_customer_profit = px.bar(
        top_profit_customers,
        x="Profit",
        y="Customer_ID",
        orientation="h",
        title="Top 10 Customers by Profit"
    )

    st.plotly_chart(
        fig_customer_profit,
        use_container_width=True
    )
# -----------------------------
# Data table
# -----------------------------
st.subheader("Sales Data")

st.dataframe(
    filtered_df.sort_values("Order_Date", ascending=False),
    use_container_width=True
)
# -----------------------------
# Download filtered data
# -----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)