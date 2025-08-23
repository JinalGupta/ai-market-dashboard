# utils/preprocessing.py

import pandas as pd

def clean_timeseries(df, date_col, value_col):
    """
    Cleans a time series dataframe:
    - Ensures correct datetime format
    - Sorts by date
    - Drops NA values
    """
    if df is None or df.empty:
        return None

    df = df.reset_index()

    # Normalize column names for safety
    df.columns = [str(c).lower().strip() for c in df.columns]
    date_col = date_col.lower().strip()
    value_col = value_col.lower().strip()

    if date_col not in df.columns:
        raise KeyError(f"Date column '{date_col}' not found in DataFrame. Available: {df.columns.tolist()}")

    if value_col not in df.columns:
        raise KeyError(f"Value column '{value_col}' not found in DataFrame. Available: {df.columns.tolist()}")

    df = df[[date_col, value_col]].dropna()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.sort_values(by=date_col)

    return df

   

def normalize_text(text):
    """
    Simple text normalization:
    - lowercase
    - strip spaces
    """
    return text.lower().strip()
