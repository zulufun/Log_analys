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
        self.setWindowTitle("Log Analyzer")
        self.setGeometry(200, 100, 1100, 700)

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

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        btn_home = QPushButton("🏠 Trang chủ")
        btn_upload = QPushButton("📤 Upload file")
        btn_result = QPushButton("📊 Kết quả")
        btn_stats = QPushButton("📈 Thống kê")
        for btn in [btn_home, btn_upload, btn_result, btn_stats]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("font-size: 16px;")
            self.sidebar_layout.addWidget(btn)
        self.sidebar_layout.addStretch()

        btn_home.clicked.connect(lambda: self.navigate_to("home"))
        btn_upload.clicked.connect(lambda: self.navigate_to("upload"))
        btn_result.clicked.connect(lambda: self.navigate_to("result"))
        btn_stats.clicked.connect(lambda: self.navigate_to("stats"))

        # Layout tổng
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.sidebar, 0)
        main_layout.addWidget(self.stack, 1)  # stack co giãn tối đa
        self.setCentralWidget(container)

        # Mặc định hiện home_page
        self.stack.setCurrentIndex(0)

    def navigate_to(self, page_name, data=None):
        """
        Hàm được gọi bởi các page để chuyển trang:
        - page_name: "home", "upload", "result", "stats"
        - data: có thể dùng để truyền kết quả giữa các page (ví dụ: path file, kết quả model)
        """
        if page_name == "home":
            self.stack.slide_to_index(0)
        elif page_name == "upload":
            self.stack.slide_to_index(1)
        elif page_name == "result":
            # Trước khi show result_page, có thể truyền data cho nó
            if data:
                self.result_page.set_result_data(data)
            self.stack.slide_to_index(2)
        elif page_name == "stats":
            if data:
                self.stats_page.set_stats_data(data)
            self.stack.slide_to_index(3)
