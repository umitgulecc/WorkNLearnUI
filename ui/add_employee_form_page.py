from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class AddEmployeeForm(QDialog):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api

        self.setWindowTitle("Yeni Çalışan Ekle")
        self.setFixedSize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(SPACING)
        layout.setContentsMargins(*MARGINS)

        # Form container
        form_container = QFrame()
        form_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
            QLineEdit {{
                background-color: {COLORS['background']};
                border: 2px solid {COLORS['primary']};
                border-radius: 5px;
                padding: 10px;
                color: {COLORS['text']};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent']};
            }}
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(SPACING)

        # Title
        title = QLabel("👤 Yeni Çalışan Ekle")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)

        # Name input
        name_label = QLabel("Ad Soyad")
        name_label.setFont(DEFAULT_FONT)
        name_label.setStyleSheet(f"color: {COLORS['text']};")
        form_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setFont(DEFAULT_FONT)
        self.name_input.setPlaceholderText("Ad Soyad")
        form_layout.addWidget(self.name_input)

        # Email input
        email_label = QLabel("E-posta")
        email_label.setFont(DEFAULT_FONT)
        email_label.setStyleSheet(f"color: {COLORS['text']};")
        form_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setFont(DEFAULT_FONT)
        self.email_input.setPlaceholderText("E-posta")
        form_layout.addWidget(self.email_input)

        # Password input
        password_label = QLabel("Şifre")
        password_label.setFont(DEFAULT_FONT)
        password_label.setStyleSheet(f"color: {COLORS['text']};")
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setFont(DEFAULT_FONT)
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)

        # Department input
        department_label = QLabel("Departman")
        department_label.setFont(DEFAULT_FONT)
        department_label.setStyleSheet(f"color: {COLORS['text']};")
        form_layout.addWidget(department_label)

        self.department_input = QLineEdit()
        self.department_input.setFont(DEFAULT_FONT)
        self.department_input.setPlaceholderText("Departman Adı")
        form_layout.addWidget(self.department_input)

        # Submit button
        self.submit_btn = QPushButton("✅ Kaydet")
        self.submit_btn.setFont(DEFAULT_FONT)
        self.submit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                color: {COLORS['text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #7FD17F;
                color: {COLORS['white']};
            }}
        """)
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.clicked.connect(self.register_employee)
        form_layout.addWidget(self.submit_btn)

        layout.addWidget(form_container)

    def register_employee(self):
        departments = self.api.get_departments()
        department_name = self.to_upper_english(self.department_input.text().strip())

        department_id = next((d["id"] for d in departments if self.to_upper_english(d["name"]) == department_name), None)

        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not name or not email or not password:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        try:
            if department_id is None:
                QMessageBox.warning(self, "Hata", "Girilen departman adı geçersiz.")
                return

            response = self.api.post("/register", json={
                "email": email,
                "full_name": name,
                "password": password,
                "role_id": 3,
                "department_id": department_id
            })

            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Başarılı", data["message"])

                # ✅ Başarılı kayıt sonrası tabloyu yenile
                if hasattr(self.main_app, "manager_dashboard_page"):
                    self.main_app.manager_dashboard_page.refresh_team_summary()

                self.accept()  # formu kapat
            else:
                QMessageBox.warning(self, "Hata", f"Kayıt başarısız: {response.text}")

        except Exception as e:
            QMessageBox.critical(self, "Sunucu Hatası", str(e))

    @staticmethod
    def to_upper_english(text: str) -> str:
        replacements = {
            'ç': 'c', 'Ç': 'C',
            'ğ': 'g', 'Ğ': 'G',
            'ı': 'i', 'I': 'I',
            'i': 'i', 'İ': 'I',
            'ö': 'o', 'Ö': 'O',
            'ş': 's', 'Ş': 'S',
            'ü': 'u', 'Ü': 'U'
        }
        for turkish, english in replacements.items():
            text = text.replace(turkish, english)
        return text.upper()

    def closeEvent(self, event):
        if hasattr(self.main_app, "manager_dashboard_page"):
            self.main_app.manager_dashboard_page.refresh_team_summary()
        super().closeEvent(event)
