import pandas as pd
import numpy as np
from datetime import timedelta
from app.forecasting.advanced_forecasting import forecast_with_features
import matplotlib.pyplot as plt

# Step 1: Generate Sample Dairy Demand Data (Multiple Products, 6 Months)
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", end="2025-06-30", freq='D')
products = [
    {"name": "milk", "base": 1200, "min": 800},
    {"name": "curd", "base": 400, "min": 200},
    {"name": "paneer", "base": 150, "min": 80}
]
data = []
for prod in products:
    for date in dates:
        base = np.random.normal(loc=prod["base"], scale=prod["base"] * 0.08)
        # Weekend spike for milk, festival spike for paneer, summer spike for curd
        if prod["name"] == "milk" and date.weekday() in [5, 6]:
            base += np.random.randint(100, 300)
        if prod["name"] == "curd" and date.month in [4, 5, 6]:  # Summer
            base += np.random.randint(30, 80)
        if prod["name"] == "paneer" and date.day in [1, 15, 25]:  # Simulate festival
            base += np.random.randint(40, 100)
        demand = max(prod["min"], int(base))
        data.append({
            "date": date.strftime('%Y-%m-%d'),
            "product": prod["name"],
            "demand": demand
        })
df = pd.DataFrame(data)
df.to_csv("sample_dairy_demand.csv", index=False)

# Step 2: Forecast Using Advanced Prophet for Each Product (with features, chart, and report)
results = []
for prod in [p["name"] for p in products]:
    df_prod = df[df["product"] == prod].copy()
    plot_path = f"forecast_{prod}.png"
    forecast = forecast_with_features(df_prod, periods=30, plot_path=plot_path)
    forecast["product"] = prod
    results.append(forecast.tail(10))
    # Alert logic: notify if forecasted demand > threshold
    threshold = 1400 if prod == "milk" else (500 if prod == "curd" else 250)
    alert = forecast[forecast["yhat"] > threshold]
    if not alert.empty:
        print(f"ALERT: {prod.capitalize()} demand exceeds threshold on these dates:")
        print(alert[["ds", "yhat"]][alert["ds"] > df_prod["date"].max()].to_string(index=False))
    print(f"Forecast chart saved to {plot_path}")

# Output last 10 forecasted results for each product
print("\nForecast for the next 10 days for each product:")
for res in results:
    print(res.to_string(index=False))

# Save all forecasts to CSV
all_forecasts = pd.concat(results)
all_forecasts.to_csv("forecasted_dairy_demand.csv", index=False)
print("Forecast report saved to forecasted_dairy_demand.csv")
