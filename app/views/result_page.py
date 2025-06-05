# app/views/result_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class ResultPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.result_data = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.title = QLabel("<h2>Analysis Result</h2>")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-top: 30px;")
        self.sub = QLabel("<h3>Result - KẾT QUẢ PHÂN TÍCH</h3>")
        self.sub.setStyleSheet("font-size: 20px; color: #0077cc; margin-bottom: 30px;")
        self.lbl_model = QLabel("")
        self.lbl_model.setStyleSheet("font-size: 14px; color: #555; margin-bottom: 10px;")
        self.txt_summary = QTextEdit()
        self.txt_summary.setReadOnly(True)
        self.txt_summary.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.sub)
        self.layout.addWidget(self.lbl_model)
        self.layout.addWidget(self.txt_summary)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_result_data(self, data):
        """
        Hàm này được Router gọi trước khi hiện trang Result.
        data là dict như trong analyze_log_file:
            {
                "total_lines": int,
                "counts": {"INFO": 10, "ERROR": 2, ...},
                "stats_df": DataFrame,
                "huggingface_result": ...
            }
        """
        self.result_data = data
        self._update_view()

    def _update_view(self):
        if not self.result_data:
            self.lbl_model.setText("")
            self.txt_summary.setText("Chưa có dữ liệu phân tích. Hãy upload và phân tích file log!")
            return
        data = self.result_data
        text = f"Total log lines: {data['total_lines']}\n"
        text += "Counts by level:\n"
        for lvl, cnt in data["counts"].items():
            text += f"  - {lvl}: {cnt}\n"
        # Hiển thị kết quả Hugging Face nếu có
        if data.get("huggingface_result") is not None:
            text += "\n[Hugging Face Sentiment - Dòng đầu tiên]:\n"
            text += f"{data['huggingface_result']}\n"
        self.txt_summary.setText(text)
        # Hiển thị tên model
        if data.get("model_name"):
            self.lbl_model.setText(f"Model sử dụng: <b>{data['model_name']}</b>")
        else:
            self.lbl_model.setText("")
