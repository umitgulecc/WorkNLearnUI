from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QFormLayout, QMessageBox, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class AddMembersPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.setup_ui()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(SPACING)
        layout.setContentsMargins(*MARGINS)
        layout.setAlignment(Qt.AlignTop)

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
        title = QLabel("👥 Yeni Kullanıcı Ekle")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title)

        # Back button
        back_btn = QPushButton("← Geri")
        back_btn.setFont(DEFAULT_FONT)
        back_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.main_app.setCurrentWidget(self.main_app.dashboard))
        header_layout.addWidget(back_btn)

        layout.addWidget(header_container)

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
            QComboBox {{
                background-color: {COLORS['background']};
                border: 2px solid {COLORS['primary']};
                border-radius: 5px;
                padding: 10px;
                color: {COLORS['text']};
                font-size: 14px;
            }}
            QComboBox:focus {{
                border: 2px solid {COLORS['accent']};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {COLORS['text']};
                margin-right: 5px;
            }}
            QLabel {{
                color: {COLORS['text']};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(SPACING)

        # Form
        form = QFormLayout()
        form.setSpacing(SPACING)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setFont(DEFAULT_FONT)
        self.name_input.setPlaceholderText("Ad Soyad")
        form.addRow("Ad Soyad:", self.name_input)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setFont(DEFAULT_FONT)
        self.email_input.setPlaceholderText("E-posta")
        form.addRow("E-Posta:", self.email_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setFont(DEFAULT_FONT)
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow("Şifre:", self.password_input)

        # Role combo
        self.role_combo = QComboBox()
        self.role_combo.setFont(DEFAULT_FONT)
        self.role_combo.addItem("Çalışan", 3)
        self.role_combo.addItem("Yönetici", 2)
        self.role_combo.addItem("Genel Müdür", 1)
        form.addRow("Rol:", self.role_combo)

        # Department combo
        self.department_combo = QComboBox()
        self.department_combo.setFont(DEFAULT_FONT)
        self.department_combo.addItem("Yazılım", 1)
        self.department_combo.addItem("İK", 2)
        self.department_combo.addItem("Pazarlama", 3)
        form.addRow("Departman:", self.department_combo)

        form_layout.addLayout(form)

        # Add user button
        add_btn = QPushButton("➕ Ekle")
        add_btn.setFont(DEFAULT_FONT)
        add_btn.setStyleSheet(f"""
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
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.submit_user)
        form_layout.addWidget(add_btn)

        layout.addWidget(form_container)

        self.role_combo.currentIndexChanged.connect(self.toggle_department_visibility)
        self.toggle_department_visibility()  # Check department on first selection

    def toggle_department_visibility(self):
        role_id = self.role_combo.currentData()
        is_admin = role_id == 1
        self.department_combo.setVisible(not is_admin)

    def submit_user(self):
        full_name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role_id = self.role_combo.currentData()
        department_id = self.department_combo.currentData() if role_id != 1 else None

        if not (full_name and email and password):
            QMessageBox.warning(self, "Eksik Bilgi", "Tüm alanları doldurmalısınız.")
            return

        try:
            response = self.api.post("/register", json={
                "email": email,
                "full_name": full_name,
                "password": password,
                "role_id": role_id,
                "department_id": department_id
            })

            data = response.json()

            if response.status_code == 200 and data.get("success"):
                QMessageBox.information(self, "Başarılı", "Kullanıcı eklendi.")
                self.name_input.clear()
                self.email_input.clear()
                self.password_input.clear()
            else:
                detail = data.get("detail", "Bilinmeyen hata")
                QMessageBox.critical(self, "Hata", f"Kullanıcı eklenemedi:\n{detail}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İstek sırasında hata oluştu:\n{str(e)}")
