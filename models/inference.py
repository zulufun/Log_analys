# app/model/inference.py
import pandas as pd
from app.services.statistics import compute_statistics
from transformers import pipeline

def analyze_log_file(raw_data):
    """
    Ví dụ:
    - raw_data có thể là danh sách các dòng log (strings).
    - Ở đây mình giả lập: 
        + Đếm số dòng log
        + Phân loại mức độ cảnh báo (INFO, WARN, ERROR)
    - Sau đó trả về dict chứa stats + DataFrame để hiển thị biểu đồ.
    """
    # Chuyển raw_data (list of strings) vào DataFrame tạm
    df = pd.DataFrame({"line": raw_data})
    
    # Giả sử mỗi dòng log có dạng "[<LEVEL>] message"
    df["level"] = df["line"].str.extract(r"\[([A-Z]+)\]")
    df["level"] = df["level"].fillna("UNKNOWN")

    # Đếm số dòng, số mỗi mức độ
    total_lines = len(df)
    counts = df["level"].value_counts().to_dict()

    # Tính thống kê chi tiết (service)
    stats_df = compute_statistics(df)

    # Trả về kết quả: 
    # - summary: dict 
    # - stats_df: DataFrame, để trang StatsPage hiển thị biểu đồ
    return {
        "total_lines": total_lines,
        "counts": counts,
        "stats_df": stats_df
    }

sentiment_pipeline = pipeline("sentiment-analysis", framework="pt", device=-1)
