# app/services/statistics.py
import pandas as pd

def compute_statistics(df):
    """
    Nhận vào DataFrame có cột "level".
    Trả về DataFrame gồm tần suất (counts) từng level, dùng để vẽ biểu đồ.
    """
    counts = df["level"].value_counts().reset_index()
    counts.columns = ["level", "count"]
    return counts
