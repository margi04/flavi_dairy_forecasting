import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def prepare_series(data, sku):
    series = data[data['sku'] == sku].groupby('date')['quantity'].sum()
    return series.asfreq('D').fillna(0)

def train_arima(series, order=(1,1,1)):
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    return model_fit

def forecast_demand(model_fit, steps=30):
    forecast = model_fit.forecast(steps=steps)
    return forecast
