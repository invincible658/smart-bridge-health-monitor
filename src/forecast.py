"""
ARIMA time-series forecasting module:
Models sequential dominant frequencies to forecast structural stiffness degradation trends.
"""
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

def forecast_stiffness_trend(series: pd.Series, order=(1, 1, 1), steps: int = 14):
    """
    Fits an ARIMA model on modal frequency series and forecasts future trajectory.
    """
    model = ARIMA(series, order=order)
    fitted = model.fit()
    forecast_res = fitted.get_forecast(steps=steps)
    
    mean_pred = forecast_res.predicted_mean
    conf_int = forecast_res.conf_int(alpha=0.05)
    return mean_pred, conf_int
