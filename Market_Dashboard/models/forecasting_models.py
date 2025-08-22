import pandas as pd
from prophet import Prophet

def forecast_trends(df, date_col="ds", value_col="y", periods=7):
    df = df.rename(columns={date_col: "ds", value_col: "y"})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
