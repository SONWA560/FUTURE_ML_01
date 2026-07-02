# Sales & Demand Forecasting for a UK Online Retailer

A sales forecasting project built for the Future Interns Machine Learning Task 1 (2026) brief: predict
future sales/demand from historical data and present it in a way a store owner, startup founder, or
business manager could act on.

**Primary deliverable:** [`notebooks/01_sales_forecasting.ipynb`](notebooks/01_sales_forecasting.ipynb) —
open it top to bottom for the full story: data cleaning, feature engineering, model training and
evaluation, a 30-day forecast, and a plain-English business narrative.

## What this project does

- Cleans ~542,000 raw e-commerce transactions down to a trustworthy daily revenue series
- Engineers time-based features — calendar, cyclical (day-of-week/month), trend, lags, rolling stats,
  UK holiday flag — using only pandas/NumPy (no `statsmodels`/`prophet`)
- Trains and evaluates three models (naive lag-7 baseline, Linear Regression, Random Forest) on a
  chronological 56-day holdout
- Recursively forecasts the next 30 days of revenue
- Produces seven business-facing charts and a data-driven explanation of what the forecast means for
  inventory, cash flow, and staffing decisions

## Dataset

[UCI Online Retail](https://archive.ics.uci.edu/ml/datasets/online+retail) — ~541,909 line-item
transactions from a UK-based online retailer, December 2010 to December 2011. Chosen because it's real
transaction data, downloads directly with no authentication, and is one of the task brief's three
recommended dataset options.

## Key results

- **Best model:** Linear Regression, beating the naive "same day last week" baseline on MAE, RMSE, and MAPE
- **Holdout accuracy:** ~£10,500/day mean absolute error (~28% of the holdout period's average daily revenue)
- **30-day forecast:** ~£45,300/day average, continuing the growth trend visible since September 2011
- See `outputs/figures/` for all charts, and notebook §10 for the full business write-up

| Figure | What it shows |
|---|---|
| `01_historical_trend.png` | A year of daily revenue with a 7-day rolling average |
| `02_monthly_seasonality.png` | Monthly totals — the Nov/Dec holiday peak |
| `03_day_of_week.png` | Average revenue by day of week |
| `04_actual_vs_predicted.png` | Model performance on the 56-day holdout |
| `05_residuals.png` | Error analysis — is the model's error random or biased? |
| `06_future_forecast.png` | The headline chart: next 30 days, with a historical-error band |
| `07_top_products_countries.png` | Top products and markets (descriptive) |

## Project structure

```
FUTURE_ML_01/
├── notebooks/01_sales_forecasting.ipynb   # primary deliverable
├── src/
│   ├── viz_style.py                       # shared chart styling
│   └── forecasting.py                     # recursive multi-step forecast function
├── data/
│   ├── raw/online_retail.xlsx             # downloaded source data
│   └── processed/daily_revenue.csv        # cleaned daily revenue series
├── outputs/figures/                       # exported charts (PNG, 150dpi)
└── requirements.txt
```

## Reproducing this

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/01_sales_forecasting.ipynb
```

The raw dataset is already included in `data/raw/`; to re-download it fresh:

```bash
curl -L -o data/raw/online_retail.xlsx \
  "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
```
