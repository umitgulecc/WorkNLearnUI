# ui/login_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from utils.style import APP_STYLE
from api_client import APIClient

class LoginPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = self.main_app.api
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("WORK-N-LEARN")
        title.setFont(QFont("Poppins", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.department_combo = QComboBox()
        self.layout().addWidget(self.department_combo)
        self.load_departments()
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.login)

        
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.department_combo)
        layout.addWidget(self.login_button)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        department_id = self.department_combo.currentData()
        
        result = self.api.login(email, password, department_id)

        if result["success"]:
            print("✅ Giriş başarılı, token:", self.api.token)
            self.main_app.show_role_dashboard(result["user"])
        else:
            print("❌ Giriş başarısız:", result["detail"])


    def load_departments(self):
        departments = self.api.get_departments()
        for dept in departments:
            self.department_combo.addItem(dept["name"], dept["id"])
