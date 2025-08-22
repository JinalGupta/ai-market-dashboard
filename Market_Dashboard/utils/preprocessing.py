# utils/preprocessing.py

import pandas as pd

def clean_timeseries(df, date_col, value_col):
    """
    Cleans a time series dataframe:
    - Ensures correct datetime format
    - Sorts by date
    - Drops NA values
    """
    df = df[[date_col, value_col]].dropna()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col)
    return df.reset_index(drop=True)


def normalize_text(text):
    """
    Simple text normalization:
    - lowercase
    - strip spaces
    """
    return text.lower().strip()
