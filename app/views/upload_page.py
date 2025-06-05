# app/views/upload_page.py
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from app.services.file_handler import read_log_file
from app.model.inference import analyze_log_file

class LogAnalysisThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    def __init__(self, raw_data):
        super().__init__()
        self.raw_data = raw_data
    def run(self):
        try:
            result = analyze_log_file(self.raw_data)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class UploadPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.selected_path = None
        self.analysis_thread = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        lbl = QLabel("<h2>Step 1: Choose a log file to upload</h2>")
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; margin-top: 30px;")
        sub = QLabel("<h3>Upload Log File - UPLOAD PAGE</h3>")
        sub.setStyleSheet("font-size: 20px; color: #0077cc; margin-bottom: 30px;")
        main_layout.addWidget(lbl, alignment=Qt.AlignHCenter)
        main_layout.addWidget(sub, alignment=Qt.AlignHCenter)

        # Nút browse và analyze căn giữa, co giãn tốt
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter)
        self.btn_browse = QPushButton("Browse Log File")
        self.btn_browse.setStyleSheet("font-size: 18px;")
        self.btn_browse.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_browse.clicked.connect(self.browse_file)
        self.btn_analyze = QPushButton("Analyze with Model")
        self.btn_analyze.setStyleSheet("font-size: 18px;")
        self.btn_analyze.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.clicked.connect(self.run_analysis)
        btn_layout.addWidget(self.btn_browse)
        btn_layout.addSpacing(20)
        btn_layout.addWidget(self.btn_analyze)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def browse_file(self):
        # Chỉ cho phép chọn file .log hoặc .txt
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Log File", os.getcwd(), "Log Files (*.log *.txt)")
        if file_path:
            self.selected_path = file_path
            QMessageBox.information(self, "Selected", f"Selected file:\n{file_path}")
            self.btn_analyze.setEnabled(True)

    def run_analysis(self):
        if not self.selected_path:
            return
        # Đọc file (service)
        try:
            raw_data = read_log_file(self.selected_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot read file:\n{e}")
            return
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.setText("Analyzing...")
        self.analysis_thread = LogAnalysisThread(raw_data)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.start()

    def on_analysis_finished(self, result):
        self.btn_analyze.setEnabled(True)
        self.btn_analyze.setText("Analyze with Model")
        self.router.navigate_to("result", data=result)

    def on_analysis_error(self, error_msg):
        self.btn_analyze.setEnabled(True)
        self.btn_analyze.setText("Analyze with Model")
        QMessageBox.critical(self, "Error", f"Error during analysis:\n{error_msg}")
