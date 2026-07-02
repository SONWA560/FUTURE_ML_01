"""Recursive multi-step forecasting: lag/rolling features don't exist for future
dates, so each step's features are built from real history plus the predictions
made so far, then fed back in for the next step."""

import numpy as np
import pandas as pd


def _future_row(date: pd.Timestamp, extended: pd.Series, holidays_calendar, series_start: pd.Timestamp) -> dict:
    dow = date.dayofweek
    day = pd.Timedelta(days=1)
    return {
        "day_of_week": dow,
        "is_weekend": int(dow >= 5),
        "day_of_month": date.day,
        "month": date.month,
        "quarter": date.quarter,
        "week_of_year": int(date.isocalendar()[1]),
        "is_month_start": int(date.is_month_start),
        "is_month_end": int(date.is_month_end),
        "dow_sin": np.sin(2 * np.pi * dow / 7),
        "dow_cos": np.cos(2 * np.pi * dow / 7),
        "month_sin": np.sin(2 * np.pi * date.month / 12),
        "month_cos": np.cos(2 * np.pi * date.month / 12),
        "trend_idx": (date - series_start).days,
        "lag_1": extended.loc[date - 1 * day],
        "lag_7": extended.loc[date - 7 * day],
        "lag_14": extended.loc[date - 14 * day],
        "rolling_mean_7": extended.loc[date - 7 * day : date - day].mean(),
        "rolling_mean_28": extended.loc[date - 28 * day : date - day].mean(),
        "rolling_std_7": extended.loc[date - 7 * day : date - day].std(),
        "is_holiday": int(date in holidays_calendar) if holidays_calendar is not None else 0,
    }


def forecast_future(
    model,
    history_revenue: pd.Series,
    feature_cols: list,
    series_start: pd.Timestamp,
    horizon_days: int = 30,
    holidays_calendar=None,
) -> pd.DataFrame:
    """Forecast `horizon_days` beyond the end of `history_revenue` (a Date-indexed
    revenue series). Requires at least the last 28 days of real history for the
    rolling/lag warm-up. Revenue is clipped at 0 since negative sales aren't
    meaningful. Errors compound with horizon since later predictions depend on
    earlier ones rather than real observed values."""
    extended = history_revenue.copy().sort_index()
    last_date = extended.index.max()
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")

    records = []
    for date in future_dates:
        row = _future_row(date, extended, holidays_calendar, series_start)
        x_row = pd.DataFrame([row])[feature_cols]
        pred = max(float(model.predict(x_row)[0]), 0.0)
        records.append((date, pred))
        extended.loc[date] = pred

    return pd.DataFrame(records, columns=["Date", "Forecast"]).set_index("Date")
