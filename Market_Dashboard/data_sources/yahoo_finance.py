import yfinance as yf

def get_stock_data(ticker="AMZN", period="7d", interval="1h"):
    stock = yf.download(ticker, period=period, interval=interval)
    return stock.reset_index()
