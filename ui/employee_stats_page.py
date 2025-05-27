# ui/employee_stats_page.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class EmployeeStatsPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.user = main_app.current_user
        self.setup_ui()
        self.plot_stats()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(SPACING)
        layout.setContentsMargins(*MARGINS)
        self.setLayout(layout)

        # Header container
        header_container = QFrame()
        header_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        header_layout = QHBoxLayout(header_container)

        # Title
        self.label = QLabel(f"📊 {self.user['full_name']} - Beceri Grafiği")
        self.label.setFont(TITLE_FONT)
        self.label.setStyleSheet(TITLE_STYLE)
        self.label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.label)

        # Back button
        back_btn = QPushButton("← Geri")
        back_btn.setFont(DEFAULT_FONT)
        back_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.main_app.show_role_dashboard(self.user))
        header_layout.addWidget(back_btn)

        layout.addWidget(header_container)

        # Stats container
        stats_container = QFrame()
        stats_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setSpacing(SPACING)

        # Canvas for matplotlib
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.canvas.figure.patch.set_facecolor(COLORS['white'])
        stats_layout.addWidget(self.canvas)

        layout.addWidget(stats_container)

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

        # Set background color
        ax.set_facecolor(COLORS['white'])

        # Create bars with our theme colors
        bars = ax.bar(skills, scores, color=COLORS['primary'])
        
        # Customize the plot
        ax.set_ylim(0, 100)
        ax.set_ylabel("Skor (%)", color=COLORS['text'])
        ax.set_title("Beceri Dağılımı", color=COLORS['text'], pad=20)
        
        # Customize grid
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        
        # Customize ticks
        ax.tick_params(colors=COLORS['text'])
        for spine in ax.spines.values():
            spine.set_color(COLORS['text'])

        # Add value labels on top of bars
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + 1,
                f"{int(bar.get_height())}%",
                ha='center',
                color=COLORS['text']
            )

        self.canvas.draw()
