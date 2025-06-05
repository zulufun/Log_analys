# Log Analyzer App

## Cấu trúc thư mục

```
my_log_analyzer_app/
├── app/
│   ├── main.py
│   ├── controller/
│   │   └── router.py
│   ├── model/
│   │   ├── inference.py
│   │   ├── model_loader.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── statistics.py
│   │   ├── file_handler.py
│   │   └── __init__.py
│   ├── views/
│   │   ├── stats_page.py
│   │   ├── result_page.py
│   │   ├── upload_page.py
│   │   ├── home_page.py
│   │   └── __init__.py
│   ├── widgets/
│   │   ├── animated_stack.py
│   │   └── __init__.py
│   └── __init__.py
├── assets/
├── models/
│   └── inference.py
├── requirements.txt
├── run.py
└── README.md
```

## Hướng dẫn cài đặt

1. Tạo virtual environment (khuyến nghị):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # hoặc
   source venv/bin/activate  # Linux/Mac
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

3. Để demo Hugging Face, cài thêm:
   ```bash
   pip install transformers torch
   ```

## Chạy ứng dụng

```bash
python run.py
```

## Demo sử dụng Hugging Face Transformers
Ví dụ dưới đây sẽ tải model `distilbert-base-uncased` từ Hugging Face và thử phân loại văn bản mẫu:

```python
from transformers import pipeline

# Tải pipeline phân loại văn bản (sentiment-analysis)
classifier = pipeline("sentiment-analysis")

# Dữ liệu mẫu
text = "I love using this log analyzer app!"

# Dự đoán
result = classifier(text)
print(result)
# Kết quả ví dụ: [{'label': 'POSITIVE', 'score': 0.9998}]
```

Bạn có thể thay đổi `text` để thử với dữ liệu khác. Nếu muốn dùng model khác, chỉ cần thay tên model trong hàm `pipeline` hoặc truyền tham số `model="tên-model"`.

---
Nếu cần tích hợp sâu hơn vào app, hãy tạo file Python mới và sử dụng đoạn code trên, hoặc import vào các module phù hợp. 