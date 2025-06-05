# app/views/home_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.init_ui()

    def init_ui(self):
        # Main layout với proper margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Log Analyzer AI")
        title.setStyleSheet("""
            font-size: 48px; 
            font-weight: bold; 
            color: #2c3e50;
            margin: 20px 0;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Hệ thống phân tích log thông minh với AI")
        subtitle.setStyleSheet("""
            font-size: 24px; 
            color: #0077cc;
            margin-bottom: 10px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        description = QLabel("Phân tích và phát hiện anomaly trong log files một cách tự động")
        description.setStyleSheet("""
            font-size: 16px; 
            color: #666;
            margin-bottom: 30px;
        """)
        description.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(description)
        
        # Features section
        features_frame = QFrame()
        features_frame.setFrameStyle(QFrame.StyledPanel)
        features_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        features_layout = QVBoxLayout(features_frame)
        features_layout.setSpacing(15)
        
        features_title = QLabel("✨ Tính năng chính")
        features_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        features_layout.addWidget(features_title)
        
        features = [
            "🔍 Phân tích log files tự động với AI",
            "📊 Thống kê chi tiết theo log levels",
            "🎯 Phát hiện anomaly và pattern bất thường", 
            "📈 Visualization trực quan với biểu đồ",
            "⚡ Xử lý nhanh chóng với multi-threading"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("font-size: 16px; padding: 8px 0; color: #495057;")
            features_layout.addWidget(feature_label)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(20)
        
        btn_start = QPushButton("🚀 Bắt đầu phân tích")
        btn_start.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
                background-color: #0077cc;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        btn_start.setCursor(Qt.PointingHandCursor)
        btn_start.clicked.connect(lambda: self.router.navigate_to("upload"))
        
        btn_demo = QPushButton("📋 Xem demo")
        btn_demo.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
                background-color: white;
                color: #0077cc;
                border: 2px solid #0077cc;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
            }
            QPushButton:pressed {
                background-color: #cce7ff;
            }
        """)
        btn_demo.setCursor(Qt.PointingHandCursor)
        btn_demo.clicked.connect(lambda: self.router.navigate_to("stats"))
        
        buttons_layout.addWidget(btn_start)
        buttons_layout.addWidget(btn_demo)
        
        # Assemble main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(features_frame)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Set size policy for proper expansion
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)