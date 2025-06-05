# app/controller/router.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QFrame
from PyQt5.QtCore import Qt
from app.widgets.animated_stack import AnimatedStackedWidget
from app.views.home_page import HomePage
from app.views.upload_page import UploadPage
from app.views.result_page import ResultPage
from app.views.stats_page import StatsPage

class Router(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Analyzer - Hệ thống phân tích log với AI")
        self.setGeometry(200, 100, 1200, 800)
        self.setMinimumSize(1000, 600)

        # AnimatedStackedWidget chứa các page
        self.stack = AnimatedStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Khởi tạo các page
        self.home_page = HomePage(self)
        self.upload_page = UploadPage(self)
        self.result_page = ResultPage(self)
        self.stats_page = StatsPage(self)

        # Đăng ký page vào stack
        self.stack.addWidget(self.home_page)     # index 0
        self.stack.addWidget(self.upload_page)   # index 1
        self.stack.addWidget(self.result_page)   # index 2
        self.stack.addWidget(self.stats_page)    # index 3

        # Sidebar với styling tốt hơn
        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-right: 2px solid #ddd;
            }
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setSpacing(5)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar.setFixedWidth(220)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Tạo các nút navigation
        self.nav_buttons = []
        btn_home = QPushButton("🏠 Trang chủ")
        btn_upload = QPushButton("📤 Upload File")
        btn_result = QPushButton("📊 Kết quả")
        btn_stats = QPushButton("📈 Thống kê")
        
        self.nav_buttons = [btn_home, btn_upload, btn_result, btn_stats]
        
        for i, btn in enumerate(self.nav_buttons):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    background-color: white;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e6f3ff;
                    border-color: #0077cc;
                }
                QPushButton:pressed {
                    background-color: #cce7ff;
                }
            """)
            self.sidebar_layout.addWidget(btn)
        
        self.sidebar_layout.addStretch()

        # Kết nối sự kiện
        btn_home.clicked.connect(lambda: self.navigate_to("home"))
        btn_upload.clicked.connect(lambda: self.navigate_to("upload"))
        btn_result.clicked.connect(lambda: self.navigate_to("result"))
        btn_stats.clicked.connect(lambda: self.navigate_to("stats"))

        # Layout tổng với margin và spacing hợp lý
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.sidebar, 0)
        main_layout.addWidget(self.stack, 1)
        
        self.setCentralWidget(container)

        # Mặc định hiện home_page và highlight button
        self.stack.setCurrentIndex(0)
        self.highlight_current_page(0)

    def highlight_current_page(self, index):
        """Highlight nút navigation hiện tại"""
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px;
                        border: 2px solid #0077cc;
                        border-radius: 8px;
                        background-color: #e6f3ff;
                        text-align: left;
                        color: #0077cc;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px;
                        border: 2px solid #ccc;
                        border-radius: 8px;
                        background-color: white;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #e6f3ff;
                        border-color: #0077cc;
                    }
                """)

    def navigate_to(self, page_name, data=None):
        """
        Hàm được gọi bởi các page để chuyển trang:
        - page_name: "home", "upload", "result", "stats"
        - data: có thể dùng để truyền kết quả giữa các page
        """
        if page_name == "home":
            self.stack.slide_to_index(0)
            self.highlight_current_page(0)
        elif page_name == "upload":
            self.upload_page.reset_ui()  # Reset UI khi chuyển sang trang upload
            self.stack.slide_to_index(1)
            self.highlight_current_page(1)
        elif page_name == "result":
            if data:
                self.result_page.set_result_data(data)
            self.stack.slide_to_index(2)
            self.highlight_current_page(2)
        elif page_name == "stats":
            if data:
                self.stats_page.set_stats_data(data)
            self.stack.slide_to_index(3)
            self.highlight_current_page(3)