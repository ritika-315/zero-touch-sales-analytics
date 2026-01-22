import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Load data
# conn = sqlite3.connect("database.db")
# df = pd.read_sql("SELECT * FROM sales", conn)

df = pd.read_csv("processed_data/clean_train.csv")

st.title("📊 Zero-Touch Superstore Sales Dashboard")

# KPI
st.metric("Total Sales", f"${df['sales'].sum():,.2f}")

# Sales by Year
sales_year = df.groupby("order_year")["sales"].sum().reset_index()
fig1 = px.line(sales_year, x="order_year", y="sales", title="Sales Trend")
st.plotly_chart(fig1)

# Category Sales
cat_sales = df.groupby("category")["sales"].sum().reset_index()
fig2 = px.bar(cat_sales, x="category", y="sales", title="Sales by Category")
st.plotly_chart(fig2)

# Top 10 Products
st.subheader("🏆 Top 10 Products by Sales")
top_products = df.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10).reset_index()
fig3 = px.bar(top_products, x="sales", y="product_name", orientation="h", title="Top 10 Products")
st.plotly_chart(fig3)

# Cities Analysis
st.subheader("🏙️ Top 10 Cities by Sales")
top_cities = df.groupby("city")["sales"].sum().sort_values(ascending=False).head(10).reset_index()
fig4 = px.bar(top_cities, x="sales", y="city", orientation="h", title="Top Cities by Sales")
st.plotly_chart(fig4)

# Monthly Growth Metrics
st.subheader("📅 Monthly Sales Growth")
monthly_sales = df.groupby(["order_year", "order_month"])["sales"].sum().reset_index()
monthly_sales["date"] = pd.to_datetime(monthly_sales["order_year"].astype(str) + "-" + monthly_sales["order_month"].astype(str))
fig5 = px.line(monthly_sales, x="date", y="sales", title="Monthly Sales Trend")
st.plotly_chart(fig5)

# ================= FORECASTING =================
st.subheader("🔮 Sales Forecast (Next 1 Year)")
forecast_df = pd.read_csv("processed_data/sales_forecast.csv")
# Show only future predictions
future_forecast = forecast_df[forecast_df["ds"] > df["order_date"].max()]
fig_forecast = px.line(future_forecast, x="ds", y="yhat", title="Future Sales Prediction")
st.plotly_chart(fig_forecast)

# Predicted Sales
st.subheader("🔮 Actual Sales VS Predicted Sales")
actual_sales = df.groupby("order_date")["sales"].sum().reset_index()
fig_compare = px.line()
fig_compare.add_scatter(x=actual_sales["order_date"], y=actual_sales["sales"], name="Actual Sales")
fig_compare.add_scatter(x=future_forecast["ds"], y=future_forecast["yhat"], name="Predicted Sales")
st.plotly_chart(fig_compare)


# ================= BUSINESS INSIGHTS STORYTELLING =================
st.subheader("📌 Business Insights (What This Data Tells Us)")
st.write("""
### 📊 Key Insights from Sales Data:
- 🧑‍💻 **Technology category generates the highest revenue**, indicating strong demand for tech products.
- 📈 **Sales show seasonal patterns**, with certain months performing better than others.
- 🏆 **A small number of products contribute most of the revenue** (Pareto Principle 80/20 rule).
- 🌍 **Some cities dominate sales**, meaning regional marketing can increase profits.
""")

# ================= AI AUTO SUMMARY =================
st.subheader("🤖 AI Auto Business Summary")
# Calculate insights
top_category = df.groupby("category")["sales"].sum().idxmax()
top_city = df.groupby("city")["sales"].sum().idxmax()
total_sales = df["sales"].sum()
monthly_sales = df.groupby(["order_year", "order_month"])["sales"].sum()
growth = (monthly_sales.iloc[-1] - monthly_sales.iloc[0]) / monthly_sales.iloc[0] * 100

summary = f"""
### 📊 AI Business Report:

- 💰 Total sales generated: **${total_sales:,.0f}**
- 🏆 Highest revenue category: **{top_category}**
- 🌍 Top performing city: **{top_city}**
- 📈 Sales growth from start to end: **{growth:.2f}%**
- 📌 Recommendation: Focus marketing on {top_category} and expand operations in {top_city}.
"""
st.write(summary)





