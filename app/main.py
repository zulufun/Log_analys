# app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from app.controller.router import Router

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Hệ thống phân tích phát hiện xâm nhập với AI")
    router = Router()
    router.show()   # Hiện cửa sổ chính (đã được Router khởi tạo bên trong)
    return app.exec_()
