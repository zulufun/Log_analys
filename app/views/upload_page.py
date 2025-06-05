# app/views/upload_page.py
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QFileDialog, QMessageBox, QSizePolicy, QFrame, QProgressBar,
                             QTextEdit, QGroupBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from app.services.file_handler import read_log_file
from app.model.inference import analyze_log_file

class LogAnalysisThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, raw_data):
        super().__init__()
        self.raw_data = raw_data
    
    def run(self):
        try:
            self.progress.emit("Đang khởi tạo model...")
            self.msleep(500)  # Simulate loading time
            
            self.progress.emit("Đang phân tích dữ liệu...")
            result = analyze_log_file(self.raw_data)
            
            self.progress.emit("Hoàn thành!")
            self.msleep(300)
            
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class UploadPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.selected_path = None
        self.analysis_thread = None
        self.raw_data = None
        self.init_ui()

    def init_ui(self):
        # Main layout với proper margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(25)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("📤 Upload Log File")
        title.setStyleSheet("""
            font-size: 36px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Chọn file log để phân tích với AI")
        subtitle.setStyleSheet("""
            font-size: 18px; 
            color: #666;
            margin-bottom: 20px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        # File selection section
        file_group = QGroupBox("Chọn File")
        file_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
        
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(15)
        
        # File info display
        self.file_info_frame = QFrame()
        self.file_info_frame.setFrameStyle(QFrame.StyledPanel)
        self.file_info_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        self.file_info_frame.setVisible(False)
        
        file_info_layout = QVBoxLayout(self.file_info_frame)
        self.lbl_file_path = QLabel("")
        self.lbl_file_path.setStyleSheet("font-weight: bold; color: #0077cc;")
        self.lbl_file_size = QLabel("")
        self.lbl_file_size.setStyleSheet("color: #666;")
        
        file_info_layout.addWidget(self.lbl_file_path)
        file_info_layout.addWidget(self.lbl_file_size)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(15)
        
        self.btn_browse = QPushButton("📁 Chọn File Log")
        self.btn_browse.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_file)
        
        self.btn_analyze = QPushButton("🔍 Phân tích với AI")
        self.btn_analyze.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.btn_analyze.setCursor(Qt.PointingHandCursor)
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.clicked.connect(self.run_analysis)
        
        buttons_layout.addWidget(self.btn_browse)
        buttons_layout.addWidget(self.btn_analyze)
        
        # Progress section
        self.progress_frame = QFrame()
        self.progress_frame.setFrameStyle(QFrame.StyledPanel)
        self.progress_frame.setStyleSheet("""
            QFrame {
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        self.progress_frame.setVisible(False)
        
        progress_layout = QVBoxLayout(self.progress_frame)
        self.lbl_progress = QLabel("Đang xử lý...")
        self.lbl_progress.setStyleSheet("font-weight: bold; color: #1976d2;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #2196f3;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196f3;
            }
        """)
        
        progress_layout.addWidget(self.lbl_progress)
        progress_layout.addWidget(self.progress_bar)
        
        # File preview section
        preview_group = QGroupBox("Xem trước nội dung file")
        preview_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
        preview_group.setVisible(False)
        
        preview_layout = QVBoxLayout(preview_group)
        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(True)
        self.txt_preview.setMaximumHeight(200)
        self.txt_preview.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }
        """)
        preview_layout.addWidget(self.txt_preview)
        
        # Assemble layouts
        file_layout.addWidget(self.file_info_frame)
        file_layout.addLayout(buttons_layout)
        file_layout.addWidget(self.progress_frame)
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(file_group)
        main_layout.addWidget(preview_group)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Store references
        self.preview_group = preview_group

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Chọn Log File", 
            os.getcwd(), 
            "Log Files (*.log *.txt);;All Files (*.*)"
        )
        
        if file_path:
            self.selected_path = file_path
            self.display_file_info(file_path)
            self.preview_file(file_path)
            self.btn_analyze.setEnabled(True)

    def display_file_info(self, file_path):
        """Hiển thị thông tin file"""
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_str = self.format_file_size(file_size)
        
        self.lbl_file_path.setText(f"📄 {file_name}")
        self.lbl_file_size.setText(f"📊 Kích thước: {size_str}")
        self.file_info_frame.setVisible(True)

    def format_file_size(self, size_bytes):
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def preview_file(self, file_path):
        """Xem trước nội dung file"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                # Đọc 20 dòng đầu để preview
                preview_lines = []
                for i, line in enumerate(f):
                    if i >= 20:
                        break
                    preview_lines.append(line.rstrip())
                
                preview_text = "\n".join(preview_lines)
                if len(preview_lines) >= 20:
                    preview_text += "\n... (và nhiều dòng khác)"
                
                self.txt_preview.setText(preview_text)
                self.preview_group.setVisible(True)
                
        except Exception as e:
            self.txt_preview.setText(f"Không thể xem trước file: {str(e)}")
            self.preview_group.setVisible(True)

    def run_analysis(self):
        if not self.selected_path:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file log trước!")
            return
        
        # Đọc file
        try:
            self.raw_data = read_log_file(self.selected_path)
            if not self.raw_data:
                QMessageBox.warning(self, "Cảnh báo", "File trống hoặc không có dữ liệu hợp lệ!")
                return
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc file:\n{str(e)}")
            return
        
        # Bắt đầu phân tích
        self.start_analysis()

    def start_analysis(self):
        """Bắt đầu quá trình phân tích"""
        self.btn_analyze.setEnabled(False)
        self.btn_browse.setEnabled(False)
        self.progress_frame.setVisible(True)
        
        # Tạo và chạy thread
        self.analysis_thread = LogAnalysisThread(self.raw_data)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.progress.connect(self.on_progress_update)
        self.analysis_thread.start()

    def on_progress_update(self, message):
        """Cập nhật progress"""
        self.lbl_progress.setText(message)

    def on_analysis_finished(self, result):
        """Khi phân tích hoàn thành"""
        self.progress_frame.setVisible(False)
        self.btn_analyze.setEnabled(True)
        self.btn_browse.setEnabled(True)
        
        # Chuyển đến trang kết quả với dữ liệu
        self.router.navigate_to("result", data=result)
        
        # Cũng truyền stats data cho stats page
        if "stats_df" in result:
            self.router.navigate_to("stats", data=result["stats_df"])

    def on_analysis_error(self, error_msg):
        """Khi có lỗi trong quá trình phân tích"""
        self.progress_frame.setVisible(False)
        self.btn_analyze.setEnabled(True)
        self.btn_browse.setEnabled(True)
        
        QMessageBox.critical(self, "Lỗi phân tích", f"Có lỗi xảy ra:\n{error_msg}")

    def reset_ui(self):
        """Reset UI về trạng thái ban đầu và dừng thread nếu còn chạy"""
        self.selected_path = None
        self.raw_data = None
        self.file_info_frame.setVisible(False)
        self.preview_group.setVisible(False)
        self.progress_frame.setVisible(False)
        self.btn_analyze.setEnabled(False)
        self.btn_browse.setEnabled(True)
        self.txt_preview.clear()
        self.lbl_file_path.setText("")
        self.lbl_file_size.setText("")
        self.txt_preview.setText("")
        self.lbl_progress.setText("")
        if hasattr(self, 'analysis_thread') and self.analysis_thread is not None:
            try:
                self.analysis_thread.terminate()
            except Exception:
                pass
            self.analysis_thread = None