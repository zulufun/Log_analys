# app/services/file_handler.py

def read_log_file(file_path):
    """
    Đọc file log, trả về list các dòng (strings).
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("File trống hoặc không chứa dữ liệu hợp lệ.")
    return lines
