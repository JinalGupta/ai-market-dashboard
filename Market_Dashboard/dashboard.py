import streamlit as st
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
trends = get_trends(product_input)  # fetch trends using original input
trends = clean_timeseries(trends, "date", product)  # clean using normalized column
if trends is not None:
    fig_trends = px.line(trends, x="date", y=product, title=f"Search Trends for {product_input}")
    st.plotly_chart(fig_trends)
else:
    st.write("No trend data available for this product.")

# --- Forecasting ---
st.subheader("Forecasted Trends")
if trends is not None and not trends.empty:
    forecast_df = trends.rename(columns={"date": "ds", product: "y"})
    forecast = forecast_trends(forecast_df)
    fig_forecast = px.line(forecast, x="ds", y="yhat", title=f"Forecast for {product_input}")
    st.plotly_chart(fig_forecast)

# --- Stock Data ---
# Stock Data
# Stock Data
st.subheader("Stock Data (Yahoo Finance)")
stock = get_stock_data("AMZN")

# Make sure datetime is a proper column
if isinstance(stock.index, pd.DatetimeIndex):
    stock = stock.reset_index()  # move index to a column
    stock.rename(columns={stock.columns[0]: "Date"}, inplace=True)
elif "Date" not in stock.columns:
    # fallback: if neither index nor Date column exists, raise an informative error
    raise ValueError(f"Stock DataFrame does not contain a datetime column. Columns: {stock.columns.tolist()}")

# Check column names
st.write("Columns in stock data:", stock.columns.tolist())

# Plot
fig_stock = px.line(stock, x="Date", y="Close", title="Amazon Stock Price")
st.plotly_chart(fig_stock)


# --- E-commerce Pricing ---
st.subheader("E-commerce Prices")
prices = get_product_price(product_input)
if prices is not None and not prices.empty:
    fig_price = px.line(prices, x="timestamp", y="price", title=f"Price Tracking: {product_input}")
    st.plotly_chart(fig_price)

    # --- Anomaly Detection ---
    st.subheader("Anomaly Detection on Prices")
    prices_anomalies = detect_anomalies(prices.rename(columns={"price": "value"}))
    fig_anomaly = px.scatter(prices_anomalies, x="timestamp", y="value", color="anomaly", title="Price Anomalies")
    st.plotly_chart(fig_anomaly)

# --- Sentiment Analysis ---
st.subheader("Sentiment Analysis")
sample_reviews = [
    f"I love my new {product_input}!",
    f"The {product_input} is overpriced.",
    f"Best {product_input} ever released!"
]
sentiments = analyze_sentiment(sample_reviews)
st.write(sentiments)

# --- Insights ---
st.subheader("📌 AI Insights")
if trends is not None and not trends.empty:
    pct_change = trends[product].pct_change().iloc[-1] * 100
    st.write(f"🔹 {product_input} is experiencing a {pct_change:.2f}% change in search interest.")
st.write(f"🔹 Sentiment Analysis: {sentiments}")
st.write("🔹 Stock prices and e-commerce trends are visualized above.")