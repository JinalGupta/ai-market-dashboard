import numpy as np
import pandas as pd

def detect_anomalies(df, col="value", threshold=2.5):
    mean, std = df[col].mean(), df[col].std()
    df["anomaly"] = abs((df[col] - mean) / std) > threshold
    return df
