# config.py

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"   # Local MongoDB
DB_NAME = "market_dashboard"

# APIs and Settings
GOOGLE_TRENDS_GEO = "IN"       # Country code (India here)
GOOGLE_TRENDS_TIMEFRAME = "now 7-d"

YAHOO_TICKER = "AMZN"          # Example: Amazon stock

DEFAULT_PRODUCT = "iPhone"
FORECAST_PERIODS = 7
ANOMALY_THRESHOLD = 2.5
