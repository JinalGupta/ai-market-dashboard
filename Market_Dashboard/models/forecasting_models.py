import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_trends(data: pd.DataFrame, periods: int = 12):
    """
    Forecast trends using ARIMA (lightweight alternative to Prophet).
    
    Parameters:
        data (pd.DataFrame): must have columns ['ds', 'y']
        periods (int): number of future periods to forecast

    Returns:
        pd.DataFrame with ['ds', 'yhat'] forecasted values
    """
    # Ensure correct types
    data = data.copy()
    data['ds'] = pd.to_datetime(data['ds'])
    data = data.set_index('ds')

    # Fit ARIMA model
    model = ARIMA(data['y'], order=(2, 1, 2))  # You can tune (p,d,q)
    fitted = model.fit()

    # Forecast
    forecast = fitted.get_forecast(steps=periods)
    forecast_df = forecast.summary_frame()

    # Format output
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=periods, freq='D')
    result = pd.DataFrame({
        'ds': future_dates,
        'yhat': forecast_df['mean'].values
    })
    return result
