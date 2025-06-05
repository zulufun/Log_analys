# app/views/home_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class HomePage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        lbl = QLabel("<h1>Welcome to Log Analyzer</h1>")
        lbl.setStyleSheet("font-size: 32px; font-weight: bold; margin-top: 40px;")
        sub = QLabel("<h3>Trang chủ - HOME PAGE</h3>")
        sub.setStyleSheet("font-size: 20px; color: #0077cc; margin-bottom: 30px;")
        layout.addWidget(lbl)
        layout.addWidget(sub)
        layout.addStretch()
        self.setLayout(layout)
