# ui/login_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from api_client import APIClient
from .style_constants import (
    COLORS, BUTTON_STYLE, INPUT_STYLE, TITLE_STYLE,
    WINDOW_STYLE, TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class LoginPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = self.main_app.api
        self.setup_ui()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(SPACING)
        layout.setContentsMargins(*MARGINS)
        layout.setAlignment(Qt.AlignCenter)

        # Create a container frame for login form
        login_container = QFrame()
        login_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        container_layout = QVBoxLayout(login_container)
        container_layout.setSpacing(SPACING)

        # Title
        title = QLabel("WORK-N-LEARN")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignCenter)

        # Inputs
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")
        self.email_input.setFont(DEFAULT_FONT)
        self.email_input.setStyleSheet(INPUT_STYLE)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(DEFAULT_FONT)
        self.password_input.setStyleSheet(INPUT_STYLE)

        self.department_combo = QComboBox()
        self.department_combo.setFont(DEFAULT_FONT)
        self.department_combo.setStyleSheet(INPUT_STYLE)
        self.department_combo.addItem("Departman Seçiniz")
        self.department_combo.addItem("Yönetici", None)
        self.load_departments()

        # Login button
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setFont(DEFAULT_FONT)
        self.login_button.setStyleSheet(BUTTON_STYLE)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)

        # Add widgets to container
        container_layout.addWidget(title)
        container_layout.addSpacing(SPACING)
        container_layout.addWidget(self.email_input)
        container_layout.addWidget(self.password_input)
        container_layout.addWidget(self.department_combo)
        container_layout.addSpacing(SPACING // 2)
        container_layout.addWidget(self.login_button)

        # Add container to main layout
        layout.addWidget(login_container)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        department_id = self.department_combo.currentData()
        
        result = self.api.login(email, password, department_id)

        print("Giriş denemesi:", email, password, department_id)
        print("Giriş sonucu:", result)
        if result["success"]:
            print("✅ Giriş başarılı, token:", self.api.token)
            self.main_app.show_role_dashboard(result["user"])
        else:
            error_detail = result["detail"]
            # Eğer hata email geçersizliğiyse
            if error_detail and isinstance(error_detail, list) and "email" in error_detail[0]["loc"]:
                reason = error_detail[0]["msg"]
                QMessageBox.warning(self, "Geçersiz E-posta", f"E-posta formatı hatalı: {reason}")
            else:
                QMessageBox.warning(self, "Giriş Başarısız", "Giriş yapılamadı, lütfen bilgilerinizi kontrol edin.")


    def load_departments(self):
        departments = self.api.get_departments()
        for dept in departments:
            self.department_combo.addItem(dept["name"], dept["id"])
