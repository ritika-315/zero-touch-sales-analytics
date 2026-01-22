import pandas as pd
from sqlalchemy import create_engine
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
DATA_FILE = os.path.join(BASE_DIR, "processed_data", "clean_train.csv")
DB_FILE = os.path.join(BASE_DIR, "database.db")

# Connect SQLite
engine = create_engine(f"sqlite:///{DB_FILE}")

# Load cleaned data
df = pd.read_csv(DATA_FILE)

# Store in DB
df.to_sql("sales", engine, if_exists="replace", index=False)

print("✅ Data stored in database automatically!")
print("Rows inserted:", len(df))
