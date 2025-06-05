# app/views/result_page.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
                             QGroupBox, QFrame, QScrollArea, QPushButton, QSizePolicy,
                             QGridLayout, QProgressBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette

class ResultPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.result_data = None
        self.init_ui()

    def init_ui(self):
        # Main scroll area để có thể cuộn khi nội dung nhiều
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget chính chứa nội dung
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(25)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        self.title = QLabel("📊 Kết quả phân tích")
        self.title.setStyleSheet("""
            font-size: 36px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        self.title.setAlignment(Qt.AlignCenter)
        
        self.subtitle = QLabel("Chi tiết phân tích log file với AI")
        self.subtitle.setStyleSheet("""
            font-size: 18px; 
            color: #666;
            margin-bottom: 20px;
        """)
        self.subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.subtitle)
        
        # Model info section
        self.model_frame = QFrame()
        self.model_frame.setFrameStyle(QFrame.StyledPanel)
        self.model_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f5e8;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        model_layout = QHBoxLayout(self.model_frame)
        model_layout.setAlignment(Qt.AlignLeft)
        
        model_icon = QLabel("🤖")
        model_icon.setStyleSheet("font-size: 24px;")
        
        self.lbl_model = QLabel("Chưa có thông tin model")
        self.lbl_model.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #155724;
        """)
        
        model_layout.addWidget(model_icon)
        model_layout.addWidget(self.lbl_model)
        model_layout.addStretch()
        
        # Summary statistics section
        summary_group = QGroupBox("📈 Tổng quan thống kê")
        summary_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
            }
        """)
        
        summary_layout = QVBoxLayout(summary_group)
        
        # Grid layout cho các thống kê
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Tổng số dòng
        self.total_lines_frame = self.create_stat_card("📄", "Tổng số dòng", "0", "#007bff")
        stats_grid.addWidget(self.total_lines_frame, 0, 0)
        
        # Số loại log levels
        self.log_types_frame = self.create_stat_card("🏷️", "Loại log", "0", "#28a745")
        stats_grid.addWidget(self.log_types_frame, 0, 1)
        
        # Log level phổ biến nhất
        self.common_level_frame = self.create_stat_card("⭐", "Level phổ biến", "N/A", "#ffc107")
        stats_grid.addWidget(self.common_level_frame, 0, 2)
        
        summary_layout.addLayout(stats_grid)
        
        # Log levels breakdown section
        levels_group = QGroupBox("📊 Phân tích theo Log Level")
        levels_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
            }
        """)
        
        levels_layout = QVBoxLayout(levels_group)
        self.levels_container = QWidget()
        self.levels_layout = QVBoxLayout(self.levels_container)
        self.levels_layout.setSpacing(10)
        levels_layout.addWidget(self.levels_container)
        
        # AI Analysis section (nếu có)
        self.ai_group = QGroupBox("🤖 Phân tích AI")
        self.ai_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #6f42c1;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
            }
        """)
        
        ai_layout = QVBoxLayout(self.ai_group)
        
        self.ai_result_frame = QFrame()
        self.ai_result_frame.setFrameStyle(QFrame.StyledPanel)
        self.ai_result_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9ff;
                border: 1px solid #6f42c1;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        
        ai_result_layout = QVBoxLayout(self.ai_result_frame)
        
        self.lbl_ai_title = QLabel("🔍 Sentiment Analysis - Dòng log đầu tiên:")
        self.lbl_ai_title.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #6f42c1;
            margin-bottom: 10px;
        """)
        
        self.txt_ai_result = QTextEdit()
        self.txt_ai_result.setReadOnly(True)
        self.txt_ai_result.setMaximumHeight(120)
        self.txt_ai_result.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        ai_result_layout.addWidget(self.lbl_ai_title)
        ai_result_layout.addWidget(self.txt_ai_result)
        
        ai_layout.addWidget(self.ai_result_frame)
        self.ai_group.setVisible(False)  # Ẩn mặc định
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(20)
        
        btn_view_stats = QPushButton("📈 Xem biểu đồ thống kê")
        btn_view_stats.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 6px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        btn_view_stats.setCursor(Qt.PointingHandCursor)
        btn_view_stats.clicked.connect(self.view_statistics)
        
        btn_new_analysis = QPushButton("🔄 Phân tích file khác")
        btn_new_analysis.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        btn_new_analysis.setCursor(Qt.PointingHandCursor)
        btn_new_analysis.clicked.connect(lambda: self.router.navigate_to("upload"))
        
        buttons_layout.addWidget(btn_view_stats)
        buttons_layout.addWidget(btn_new_analysis)
        
        # Assemble main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.model_frame)
        main_layout.addWidget(summary_group)
        main_layout.addWidget(levels_group)
        main_layout.addWidget(self.ai_group)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        
        # Set scroll widget
        scroll.setWidget(main_widget)
        
        # Main page layout
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        self.setLayout(page_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_stat_card(self, icon, title, value, color):
        """Tạo card thống kê"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px; 
            font-weight: bold; 
            color: {color};
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
        """)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value")  # Để dễ tìm và cập nhật
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return frame

    def create_level_bar(self, level, count, total, color):
        """Tạo thanh hiển thị tỷ lệ cho mỗi log level"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Level name
        level_label = QLabel(level)
        level_label.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold; 
            color: {color};
            min-width: 80px;
        """)
        
        # Progress bar
        progress = QProgressBar()
        percentage = (count / total * 100) if total > 0 else 0
        progress.setValue(int(percentage))
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {color};
                border-radius: 3px;
                text-align: center;
                font-weight: bold;
                color: white;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        
        # Count label
        count_label = QLabel(f"{count} ({percentage:.1f}%)")
        count_label.setStyleSheet("""
            font-size: 14px; 
            font-weight: bold; 
            color: #495057;
            min-width: 100px;
        """)
        count_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(level_label)
        layout.addWidget(progress, 1)
        layout.addWidget(count_label)
        
        return frame

    def get_level_color(self, level):
        """Lấy màu cho từng log level"""
        colors = {
            "ERROR": "#dc3545",
            "WARN": "#ffc107", 
            "WARNING": "#ffc107",
            "INFO": "#17a2b8",
            "DEBUG": "#6c757d",
            "TRACE": "#6f42c1",
            "UNKNOWN": "#495057"
        }
        return colors.get(level.upper(), "#6c757d")

    def set_result_data(self, data):
        """
        Hàm được Router gọi để set dữ liệu kết quả
        """
        self.result_data = data
        self._update_view()

    def _update_view(self):
        """Cập nhật giao diện với dữ liệu mới"""
        if not self.result_data:
            self._show_no_data()
            return
        
        data = self.result_data
        
        # Cập nhật model info
        if data.get("model_name"):
            self.lbl_model.setText(f"Model AI: {data['model_name']}")
            self.model_frame.setVisible(True)
        else:
            self.model_frame.setVisible(False)
        
        # Cập nhật summary statistics
        total_lines = data.get("total_lines", 0)
        counts = data.get("counts", {})
        
        # Tổng số dòng
        total_value_label = self.total_lines_frame.findChild(QLabel, "value")
        if total_value_label:
            total_value_label.setText(str(total_lines))
        
        # Số loại log levels
        types_value_label = self.log_types_frame.findChild(QLabel, "value")
        if types_value_label:
            types_value_label.setText(str(len(counts)))
        
        # Level phổ biến nhất
        common_value_label = self.common_level_frame.findChild(QLabel, "value")
        if common_value_label and counts:
            most_common = max(counts, key=counts.get)
            common_value_label.setText(most_common)
        
        # Cập nhật log levels breakdown
        self._update_levels_breakdown(counts, total_lines)
        
        # Cập nhật AI analysis
        self._update_ai_analysis(data)

    def _update_levels_breakdown(self, counts, total_lines):
        """Cập nhật phần breakdown theo log levels"""
        # Xóa các widget cũ
        for i in reversed(range(self.levels_layout.count())):
            child = self.levels_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Thêm các thanh mới
        if not counts:
            no_data_label = QLabel("Không có dữ liệu log levels")
            no_data_label.setStyleSheet("font-size: 16px; color: #6c757d; text-align: center;")
            no_data_label.setAlignment(Qt.AlignCenter)
            self.levels_layout.addWidget(no_data_label)
            return
        
        # Sắp xếp theo số lượng giảm dần
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        for level, count in sorted_counts:
            color = self.get_level_color(level)
            level_bar = self.create_level_bar(level, count, total_lines, color)
            self.levels_layout.addWidget(level_bar)

    def _update_ai_analysis(self, data):
        """Cập nhật phần AI analysis"""
        hf_result = data.get("huggingface_result")
        
        if hf_result is not None:
            self.ai_group.setVisible(True)
            
            if isinstance(hf_result, str):
                # Có lỗi
                self.txt_ai_result.setText(f"Lỗi khi chạy AI analysis: {hf_result}")
                self.txt_ai_result.setStyleSheet("""
                    QTextEdit {
                        font-size: 14px;
                        background-color: #f8d7da;
                        border: 1px solid #f5c6cb;
                        border-radius: 4px;
                        padding: 8px;
                        color: #721c24;
                    }
                """)
            else:
                # Có kết quả
                result_text = ""
                if isinstance(hf_result, list) and len(hf_result) > 0:
                    result = hf_result[0]
                    label = result.get('label', 'Unknown')
                    score = result.get('score', 0)
                    result_text = f"Label: {label}\nConfidence: {score:.4f} ({score*100:.2f}%)"
                    
                    # Thêm emoji dựa trên kết quả
                    if label.upper() == 'POSITIVE':
                        result_text = f"😊 {result_text}"
                    elif label.upper() == 'NEGATIVE':
                        result_text = f"😟 {result_text}"
                    else:
                        result_text = f"🤔 {result_text}"
                else:
                    result_text = str(hf_result)
                
                self.txt_ai_result.setText(result_text)
                self.txt_ai_result.setStyleSheet("""
                    QTextEdit {
                        font-size: 14px;
                        background-color: white;
                        border: 1px solid #dee2e6;
                        border-radius: 4px;
                        padding: 8px;
                    }
                """)
        else:
            self.ai_group.setVisible(False)

    def _show_no_data(self):
        """Hiển thị thông báo khi chưa có dữ liệu"""
        # Reset tất cả về trạng thái ban đầu
        self.model_frame.setVisible(False)
        
        # Reset summary cards
        for frame in [self.total_lines_frame, self.log_types_frame, self.common_level_frame]:
            value_label = frame.findChild(QLabel, "value")
            if value_label:
                value_label.setText("0" if frame != self.common_level_frame else "N/A")
        
        # Clear levels breakdown
        for i in reversed(range(self.levels_layout.count())):
            child = self.levels_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        no_data_label = QLabel("Chưa có dữ liệu phân tích.\nHãy upload và phân tích file log trước!")
        no_data_label.setStyleSheet("""
            font-size: 18px; 
            color: #6c757d; 
            text-align: center;
            padding: 40px;
        """)
        no_data_label.setAlignment(Qt.AlignCenter)
        self.levels_layout.addWidget(no_data_label)
        
        # Hide AI section
        self.ai_group.setVisible(False)

    def view_statistics(self):
        """Chuyển đến trang thống kê"""
        if self.result_data and "stats_df" in self.result_data:
            self.router.navigate_to("stats", data=self.result_data["stats_df"])
        else:
            self.router.navigate_to("stats")