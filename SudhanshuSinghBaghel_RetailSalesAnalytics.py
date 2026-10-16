"""
Retail Sales Analytics & Business Intelligence Dashboard
Dataset: retail_sales_dataset.csv (included in this project folder).

Run:
    pip install -r requirements.txt
    streamlit run retail_bi_dashboard.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Retail BI Dashboard", page_icon="📊", layout="wide")
st.title("Retail Sales Analytics & Business Intelligence")
st.caption("Decision-focused dashboard | Uses the included educational dataset.")

DATA_PATH = Path(__file__).resolve().parent / "retail_sales_dataset.csv"

@st.cache_data
def load_data(path_string):
    frame = pd.read_csv(path_string)
    required = {"Order_ID", "Order_Date", "Region", "Segment", "Category", "Product",
                "Quantity", "Discount", "Sales", "Profit"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    frame["Order_Date"] = pd.to_datetime(frame["Order_Date"], errors="coerce")
    for col in ["Quantity", "Discount", "Sales", "Profit"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna(subset=["Order_Date", "Sales", "Profit", "Order_ID"])
    frame["Month"] = frame["Order_Date"].dt.to_period("M").dt.to_timestamp()
    frame["Profit_Margin"] = np.where(frame["Sales"] != 0, frame["Profit"] / frame["Sales"], 0)
    return frame

try:
    data = load_data(str(DATA_PATH))
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.info("Keep retail_sales_dataset.csv in the same folder as retail_bi_dashboard.py.")
    st.stop()

min_date, max_date = data["Order_Date"].min().date(), data["Order_Date"].max().date()
with st.sidebar:
    st.header("Filters")
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    selected_categories = st.multiselect("Product category", sorted(data["Category"].dropna().unique()),
                                         default=sorted(data["Category"].dropna().unique()))
    selected_regions = st.multiselect("Region", sorted(data["Region"].dropna().unique()),
                                      default=sorted(data["Region"].dropna().unique()))
    selected_segments = st.multiselect("Customer segment", sorted(data["Segment"].dropna().unique()),
                                       default=sorted(data["Segment"].dropna().unique()))

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = pd.Timestamp(min_date), pd.Timestamp(max_date)

filtered = data[
    data["Order_Date"].between(start_date, end_date + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1))
    & data["Category"].isin(selected_categories)
    & data["Region"].isin(selected_regions)
    & data["Segment"].isin(selected_segments)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Change one or more filters.")
    st.stop()

sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
order_count = filtered["Order_ID"].nunique()
aov = sales / order_count if order_count else 0
margin = profit / sales * 100 if sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Sales", f"${sales:,.0f}")
k2.metric("Total Profit", f"${profit:,.0f}")
k3.metric("Orders", f"{order_count:,}")
k4.metric("Average Order Value", f"${aov:,.0f}")
k5.metric("Profit Margin", f"{margin:.1f}%")

left, right = st.columns(2)
with left:
    st.subheader("Monthly sales trend")
    st.line_chart(filtered.groupby("Month")["Sales"].sum())
with right:
    st.subheader("Sales by category")
    st.bar_chart(filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False))

left2, right2 = st.columns(2)
with left2:
    st.subheader("Profit by region")
    st.bar_chart(filtered.groupby("Region")["Profit"].sum().sort_values(ascending=False))
with right2:
    st.subheader("Sales by customer segment")
    st.bar_chart(filtered.groupby("Segment")["Sales"].sum().sort_values(ascending=False))

st.subheader("Product performance")
product_table = filtered.groupby(["Category", "Product"], as_index=False).agg(
    Orders=("Order_ID", "nunique"), Units=("Quantity", "sum"),
    Sales=("Sales", "sum"), Profit=("Profit", "sum"))
product_table["Profit Margin (%)"] = np.where(
    product_table["Sales"] != 0, product_table["Profit"] / product_table["Sales"] * 100, 0)
product_table = product_table.sort_values("Sales", ascending=False)
st.dataframe(product_table.style.format({
    "Sales": "${:,.2f}", "Profit": "${:,.2f}", "Profit Margin (%)": "{:.1f}%"}),
    use_container_width=True)

st.subheader("Decision support: observations and recommended actions")
category_sales = filtered.groupby("Category")["Sales"].sum()
region_profit = filtered.groupby("Region")["Profit"].sum()
best_category = category_sales.idxmax() if len(category_sales) else "N/A"
best_region = region_profit.idxmax() if len(region_profit) else "N/A"
weak_region = region_profit.idxmin() if len(region_profit) else "N/A"
st.markdown(f"""
- **Opportunity:** **{best_category}** is the leading category by sales in the selected view. Review product mix and stock availability before increasing promotional spend.
- **Regional follow-up:** **{best_region}** leads on total profit, while **{weak_region}** is lowest in this filtered view. Investigate order mix, discounts, and costs before changing regional budgets.
- **Margin protection:** Compare profit margin alongside sales; high revenue does not automatically mean high profitability. Review discounted orders and test discount limits.
- **Next action:** Review indicators monthly, investigate unusual changes, and validate recommendations against actual business data before operational decisions.
""")
st.caption("Dataset note: this is an educational synthetic dataset created for this project, not real company data.")
