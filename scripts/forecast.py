import pandas as pd
from prophet import Prophet

df = pd.read_csv("processed_data/clean_train.csv")
sales = df.groupby("order_date")["sales"].sum().reset_index()
sales.columns = ["ds", "y"]

model = Prophet()
model.fit(sales)

future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

forecast.to_csv("processed_data/sales_forecast.csv")
print("Forecast saved!")
