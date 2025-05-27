# ui/employee_stats_page.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Qt

class EmployeeStatsPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.user = main_app.current_user

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(f"📊 {self.user['full_name']} - Beceri Grafiği")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(self.label)

        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        layout.addWidget(self.canvas)

        # Geri butonu
        back_btn = QPushButton("← Geri")
        back_btn.clicked.connect(lambda: self.main_app.show_role_dashboard(self.user))
        back_btn.setStyleSheet("padding: 8px; font-size: 14px; background-color: #4CAF50; color: white; border-radius: 6px;")
        layout.addWidget(back_btn)

        self.plot_stats()

    def plot_stats(self):
        data = {
            "Reading": 78,
            "Writing": 65,
            "Listening": 88
        }

        skills = list(data.keys())
        scores = list(data.values())

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        bars = ax.bar(skills, scores, color="#66a6ff")
        ax.set_ylim(0, 100)
        ax.set_ylabel("Skor (%)")
        ax.set_title("Beceri Dağılımı")

        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{int(bar.get_height())}%", ha='center')

        self.canvas.draw()
