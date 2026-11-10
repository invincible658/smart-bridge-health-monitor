"""
ARIMA Time-Series Forecasting Module for Structural Health Monitoring.
Models sequential modal frequency trends to forecast structural stiffness degradation
and detect projected threshold breaches.
"""
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_stiffness_trend(
    series: pd.Series,
    order: tuple = (1, 1, 0),
    steps: int = 14,
    critical_threshold_hz: float = 3.50
):
    """
    Fits an ARIMA model on a chronological sequence of modal frequencies (e.g. daily 1st bending mode).
    
    Parameters:
        series (pd.Series or np.ndarray): Historical dominant frequency values
        order (tuple): ARIMA (p, d, q) order
        steps (int): Number of future steps to forecast
        critical_threshold_hz (float): Safety threshold below which structural stiffness is compromised
        
    Returns:
        dict: Forecast mean, 95% confidence intervals, and breach prediction diagnostics
    """
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
        
    # Fit ARIMA model with stationary enforcement set to False for small sample slices
    model = ARIMA(series, order=order, enforce_stationarity=False, enforce_invertibility=False)
    fitted = model.fit()
    
    # Generate out-of-sample forecast with 95% confidence interval
    forecast_res = fitted.get_forecast(steps=steps)
    mean_forecast = forecast_res.predicted_mean.values
    conf_int = forecast_res.conf_int(alpha=0.05).values  # Shape: (steps, 2)
    
    lower_bound = conf_int[:, 0]
    upper_bound = conf_int[:, 1]
    
    # Check for projected safety threshold breach
    breach_indices = np.where(mean_forecast < critical_threshold_hz)[0]
    will_breach = len(breach_indices) > 0
    steps_to_breach = int(breach_indices[0] + 1) if will_breach else None
    
    return {
        "mean_forecast": [float(f) for f in mean_forecast],
        "lower_bound": [float(l) for l in lower_bound],
        "upper_bound": [float(u) for u in upper_bound],
        "critical_threshold_hz": float(critical_threshold_hz),
        "breach_predicted": will_breach,
        "steps_to_breach": steps_to_breach
    }
