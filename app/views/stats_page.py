# app/views/stats_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StatsPage(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.stats_df = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.title = QLabel("<h2>Statistics</h2>")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-top: 30px;")
        self.sub = QLabel("<h3>Statistics - THỐNG KÊ LOG</h3>")
        self.sub.setStyleSheet("font-size: 20px; color: #0077cc; margin-bottom: 30px;")
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("font-size: 16px; color: #555; margin-bottom: 10px;")
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(self.canvas.sizePolicy().Expanding, self.canvas.sizePolicy().Expanding)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.sub)
        self.layout.addWidget(self.lbl_info)
        self.layout.addWidget(self.canvas, stretch=1)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_stats_data(self, df):
        """
        df: DataFrame có 2 cột "level" và "count"
        """
        self.stats_df = df
        self._update_view()

    def _update_view(self):
        if self.stats_df is None:
            self.lbl_info.setText("Chưa có dữ liệu thống kê. Hãy upload và phân tích file log!")
            self.figure.clear()
            self.canvas.draw()
            return
        self.lbl_info.setText("")
        self._plot_chart()

    def _plot_chart(self):
        # Xóa plot cũ (nếu có)
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Vẽ bar chart: level vs count
        levels = self.stats_df["level"].tolist()
        counts = self.stats_df["count"].tolist()
        ax.bar(levels, counts)
        ax.set_title("Log Level Frequency")
        ax.set_xlabel("Log Level")
        ax.set_ylabel("Count")

        # Vẽ lại canvas
        self.canvas.draw()
