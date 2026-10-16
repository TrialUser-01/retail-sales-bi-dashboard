# Retail Sales Analytics & Business Intelligence Dashboard

## Project overview
This project turns retail transaction data into a decision-focused dashboard. It summarizes sales, profit, order count, average order value, profit margin, monthly trends, category performance, regional profitability, customer segments, and product-level results.

## Problem statement
Raw transaction tables can be difficult for a decision-maker to interpret quickly. This dashboard organizes core performance indicators and helps users identify areas that deserve further investigation.

## Dataset
- **File:** `retail_sales_dataset.csv`
- **Records:** 1,800 simulated retail transactions
- **Date range:** 2023-01-01 to 2025-12-31 (dates are sampled within this range)
- **Columns:** Order_ID, Order_Date, Region, Segment, Category, Product, Quantity, Discount, Sales, Profit
- **Source:** Created specifically for this educational project with a fixed random seed. It is included as a separate CSV file so the dashboard reads a dataset rather than generating records at runtime.
- **Transparency:** This is synthetic demonstration data, not a real retailer's data. It contains no real customer personal information. Do not present the sample's results as actual market findings.
- **Dataset link:** Once uploaded, the CSV will be available inside your GitHub repository as `retail_sales_dataset.csv`. The repository URL is the shareable project/data link.

## Features
- Interactive filters for date range, category, region, and customer segment
- KPI cards for total sales, profit, orders, average order value, and profit margin
- Monthly sales trend
- Sales by category and customer segment
- Profit by region
- Product performance table
- Decision-support observations and recommended follow-up actions

## Technology stack
- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib (used for report visuals)

## Installation and running
1. Install Python 3.10 or newer.
2. Keep `retail_bi_dashboard.py`, `retail_sales_dataset.csv`, and `requirements.txt` in the same folder.
3. Open a terminal in that folder and run:

   ```bash
   pip install -r requirements.txt
   streamlit run retail_bi_dashboard.py
   ```

4. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## How to use
Use the sidebar filters to select a date range, categories, regions, and customer segments. Review KPI cards and charts, inspect the product table, and use the decision-support notes to guide further investigation.

## Data definitions
- **Sales:** simulated transaction value after discount.
- **Profit:** simulated value calculated using category-level margin assumptions, a discount penalty, and random variation.
- **Average order value:** total sales divided by unique order IDs.
- **Profit margin:** total profit divided by total sales.

## Limitations and future improvements
The data is synthetic, and profit is simulated rather than based on actual accounting costs. Future improvements include replacing the CSV with a permitted public dataset, adding CSV upload and validation, enabling filtered exports, and adding forecasting only after data quality and model performance are evaluated.

## Author
Prepared as an educational data analytics project.


## Dataset link for submission
The dataset is included in this repository as `retail_sales_dataset.csv`.
After uploading the project to GitHub, replace the placeholder below with the CSV's actual **Raw** GitHub URL so the dataset link is directly accessible:

`https://raw.githubusercontent.com/TrialUser-01/retail-sales-bi-dashboard/refs/heads/main/retail_sales_dataset.csv`

Note: this is a project-specific simulated dataset created for demonstration and analysis; it is not real company data.
