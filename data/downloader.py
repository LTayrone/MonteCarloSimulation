import pandas as pd
import yfinance as yf


def normalize_columns(data):
    """Flatten Yahoo Finance multi-level columns when necessary."""
    if isinstance(data.columns, pd.MultiIndex):
        data = data.copy()
        data.columns = data.columns.get_level_values(0)

    return data


def download_data(ticker, start_date, end_date):
    """Download historical prices and return a DataFrame with flat columns."""
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    return normalize_columns(data)
