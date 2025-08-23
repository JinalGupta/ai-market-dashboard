import streamlit as st
import pandas as pd
import plotly.express as px
from data_sources.google_trends import get_trends
from data_sources.yahoo_finance import get_stock_data
from data_sources.ecommerce_scraper import get_product_price
from models.sentiment_models import analyze_sentiment
from models.forecasting_models import forecast_trends
from models.anomaly_detector import detect_anomalies
from config import DEFAULT_PRODUCT, FORECAST_PERIODS
from utils.preprocessing import clean_timeseries, normalize_text
from utils.visualization import line_chart, scatter_chart

st.set_page_config(page_title="AI Market Intelligence", layout="wide")
st.title("📊 AI-Powered Real-Time Market Intelligence Dashboard")

# --- Input Product ---
product_input = st.text_input("Enter Product/Keyword", DEFAULT_PRODUCT)
product = normalize_text(product_input)  # normalize before using

# --- Google Trends ---
st.subheader("Google Trends")
trends = get_trends(product_input)
if trends is not None and not trends.empty:
    try:
        trends = clean_timeseries(trends, "date", product)
        fig_trends = px.line(trends, x="date", y=product, title=f"Search Trends for {product_input}")
        st.plotly_chart(fig_trends)
    except KeyError:
        st.write("No trend data available for this product column.")
else:
    st.write("No trend data available for this product.")

# --- Forecasting ---
st.subheader("Forecasted Trends")
if trends is not None and not trends.empty:
    try:
        forecast_df = trends.rename(columns={"date": "ds", product: "y"})
        forecast = forecast_trends(forecast_df)
        fig_forecast = px.line(forecast, x="ds", y="yhat", title=f"Forecast for {product_input}")
        st.plotly_chart(fig_forecast)
    except Exception:
        st.write("Forecasting failed due to insufficient trend data.")

# --- Stock Data ---
st.subheader("Stock Data (Yahoo Finance)")
stock = get_stock_data("AMZN")

# Attempt to find a datetime column
datetime_col = None
for col in stock.columns:
    if pd.api.types.is_datetime64_any_dtype(stock[col]):
        datetime_col = col
        break

# If no datetime column, check if index is DatetimeIndex
if datetime_col is None and isinstance(stock.index, pd.DatetimeIndex):
    stock = stock.reset_index()
    datetime_col = stock.columns[0]

# If still no datetime column, display a message and skip plotting
if datetime_col is None:
    st.write("⚠️ Stock data does not contain a datetime column. Cannot plot stock chart.")
    st.write("Available columns:", stock.columns.tolist())
else:
    fig_stock = px.line(stock, x=datetime_col, y="Close", title="Amazon Stock Price")
    st.plotly_chart(fig_stock)


# --- E-commerce Pricing ---
st.subheader("E-commerce Prices")
prices = get_product_price(product_input)
if prices is not None and not prices.empty:
    if "timestamp" in prices.columns and "price" in prices.columns:
        fig_price = px.line(prices, x="timestamp", y="price", title=f"Price Tracking: {product_input}")
        st.plotly_chart(fig_price)

        # --- Anomaly Detection ---
        st.subheader("Anomaly Detection on Prices")
        prices_anomalies = detect_anomalies(prices.rename(columns={"price": "value"}))
        fig_anomaly = px.scatter(prices_anomalies, x="timestamp", y="value", color="anomaly", title="Price Anomalies")
        st.plotly_chart(fig_anomaly)
    else:
        st.write("E-commerce data missing required columns: 'timestamp' or 'price'.")
else:
    st.write("No e-commerce pricing data available.")

# --- Sentiment Analysis ---
st.subheader("Sentiment Analysis")
sample_reviews = [
    f"I love my new {product_input}!",
    f"The {product_input} is overpriced.",
    f"Best {product_input} ever released!"
]
try:
    sentiments = analyze_sentiment(sample_reviews)
    st.write(sentiments)
except Exception:
    st.write("Sentiment analysis failed.")

# --- Insights ---
st.subheader("📌 AI Insights")
if trends is not None and not trends.empty and product in trends.columns:
    pct_change = trends[product].pct_change().iloc[-1] * 100
    st.write(f"🔹 {product_input} is experiencing a {pct_change:.2f}% change in search interest.")
st.write(f"🔹 Sentiment Analysis: {sentiments if 'sentiments' in locals() else 'N/A'}")
st.write("🔹 Stock prices and e-commerce trends are visualized above.")
