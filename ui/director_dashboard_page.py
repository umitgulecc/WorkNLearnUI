from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class DirectorDashboardPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user_data = main_app.current_user
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        full_name = self.user_data.get("full_name", "Bilinmiyor")
        welcome = QLabel(f"👋 Hoş geldiniz, {full_name}!")
        welcome.setStyleSheet("font-size: 20px; color: white;")
        layout.addWidget(welcome)

        info = QLabel("🔧 Genel Müdür paneli henüz geliştirilme aşamasındadır.")
        info.setStyleSheet("color: white; font-size: 14px; margin-top: 20px;")
        layout.addWidget(info)
