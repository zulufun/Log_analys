try:
    from transformers import pipeline
    sentiment_pipeline = pipeline("sentiment-analysis")
except ImportError:
    sentiment_pipeline = None
