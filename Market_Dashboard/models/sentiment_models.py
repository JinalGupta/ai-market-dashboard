from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(texts):
    results = sentiment_analyzer(texts)
    return results
