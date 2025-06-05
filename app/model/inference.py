import pandas as pd
from app.services.statistics import compute_statistics
import os

def get_hf_token():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", ".env")
    env_path = os.path.abspath(env_path)
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("HF_TOKEN="):
                    return line.strip().split("=", 1)[1]
    return None

try:
    # Đọc tên model từ file config/model.txt
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "model.txt")
    config_path = os.path.abspath(config_path)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            model_name = f.read().strip()
    from transformers import pipeline
    hf_token = get_hf_token()
    if hf_token:
        sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, framework="pt", device=-1, token=hf_token)
    else:
        sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, framework="pt", device=-1)
except ImportError:
    sentiment_pipeline = None


def analyze_log_file(raw_data):
    """
    - raw_data: list các dòng log (strings)
    - Phân tích thống kê như cũ
    - Nếu có Hugging Face, chạy thử cảm xúc dòng đầu tiên
    """
    df = pd.DataFrame({"line": raw_data})
    df["level"] = df["line"].str.extract(r"\[([A-Z]+)\]")
    df["level"] = df["level"].fillna("UNKNOWN")
    total_lines = len(df)
    counts = df["level"].value_counts().to_dict()
    stats_df = compute_statistics(df)

    # Demo Hugging Face sentiment
    hf_result = None
    if sentiment_pipeline and len(raw_data) > 0:
        try:
            hf_result = sentiment_pipeline(raw_data[0])
        except Exception as e:
            hf_result = str(e)

    return {
        "total_lines": total_lines,
        "counts": counts,
        "stats_df": stats_df,
        "huggingface_result": hf_result,
        "model_name": model_name
    }
