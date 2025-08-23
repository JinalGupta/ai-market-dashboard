import streamlit as st
import plotly.express as px
from data_sources.google_trends import get_trends
from data_sources.yahoo_finance import get_stock_data
from data_sources.ecommerce_scraper import get_product_price
from models.sentiment_models import analyze_sentiment
from models.forecasting_models import forecast_trends
from models.anomaly_detector import detect_anomalies
from config import DEFAULT_PRODUCT, FORECAST_PERIODS
from utils.preprocessing import clean_timeseries
from utils.visualization import line_chart, scatter_chart

st.set_page_config(page_title="AI Market Intelligence", layout="wide")

st.title("📊 AI Market Intelligence Dashboard")

# Use default product from config
product = st.text_input("Enter Product", DEFAULT_PRODUCT)

# Get trends
trends = get_trends(product)
trends = clean_timeseries(trends, "date", product)

# Show chart
st.plotly_chart(line_chart(trends, "date", product, f"Google Trends for {product}"))

st.title("📊 AI-Powered Real-Time Market Intelligence Dashboard")

# Input
product = st.text_input("Enter Product/Keyword", "iPhone")

# Google Trends
st.subheader("Google Trends")
trends = get_trends(product)
fig_trends = px.line(trends, x="date", y=product, title=f"Search Trends for {product}")
st.plotly_chart(fig_trends)

# Forecasting
st.subheader("Forecasted Trends")
forecast = forecast_trends(trends.rename(columns={"date": "ds", product: "y"}))
fig_forecast = px.line(forecast, x="ds", y="yhat", title=f"Forecast for {product}")
st.plotly_chart(fig_forecast)

# Stock Data
st.subheader("Stock Data (Yahoo Finance)")
stock = get_stock_data("AMZN")
fig_stock = px.line(stock, x="Datetime", y="Close", title="Amazon Stock Price")
st.plotly_chart(fig_stock)

# E-commerce Pricing
st.subheader("E-commerce Prices")
prices = get_product_price(product)
fig_price = px.line(prices, x="timestamp", y="price", title=f"Price Tracking: {product}")
st.plotly_chart(fig_price)

# Sentiment Analysis
st.subheader("Sentiment Analysis")
sample_reviews = [
    f"I love my new {product}!",
    f"The {product} is overpriced.",
    f"Best {product} ever released!"
]
sentiments = analyze_sentiment(sample_reviews)
st.write(sentiments)

# Anomaly Detection
st.subheader("Anomaly Detection on Prices")
prices_anomalies = detect_anomalies(prices.rename(columns={"price": "value"}))
fig_anomaly = px.scatter(prices_anomalies, x="timestamp", y="value", color="anomaly", title="Price Anomalies")
st.plotly_chart(fig_anomaly)

# Example Insights
st.subheader("📌 AI Insights")
st.write(f"🔹 {product} is experiencing a {trends[product].pct_change().iloc[-1]*100:.2f}% change in search interest.")
st.write(f"🔹 Sentiment Analysis: {sentiments}")
