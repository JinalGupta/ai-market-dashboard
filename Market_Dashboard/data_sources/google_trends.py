import time
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

def get_trends(keyword, timeframe="today 3-m", geo="IN"):
    try:
        time.sleep(2)  # wait before request to avoid rate limit
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
        data = pytrends.interest_over_time()
        if not data.empty:
            return data.drop(columns=["isPartial"])
        return None
    except Exception as e:
        print("Google Trends Error:", e)
        return None
