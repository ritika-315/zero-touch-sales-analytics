import pandas as pd
import os

RAW_FILE = "raw_data/train.csv"
OUTPUT_FILE = "processed_data/clean_train.csv"

# Load data
df = pd.read_csv(RAW_FILE)

# Clean column names
df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")

# Convert dates
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)
df["ship_date"] = pd.to_datetime(df["ship_date"], dayfirst=True)

# Feature engineering (VERY IMPORTANT FOR ANALYTICS)
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["order_day"] = df["order_date"].dt.day
df["order_weekday"] = df["order_date"].dt.day_name()

# Remove duplicates & missing values
df = df.drop_duplicates()
df = df.dropna()

# Save cleaned file
df.to_csv(OUTPUT_FILE, index=False)
print("✅ Clean data saved automatically!")

