from pytrends.request import TrendReq

def get_trends(keyword: str, timeframe="now 7-d", geo="IN"):
    pytrends = TrendReq(hl="en-US", tz=330)
    pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
    data = pytrends.interest_over_time()
    return data.reset_index()
