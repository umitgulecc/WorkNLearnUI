from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class AddMembersPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.setStyleSheet(APP_STYLE)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("👥 Yeni Kullanıcı Ekle")
        title.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(title)

        form = QFormLayout()

        self.name_input = QLineEdit()
        form.addRow("Ad Soyad:", self.name_input)

        self.email_input = QLineEdit()
        form.addRow("E-Posta:", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow("Şifre:", self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItem("Çalışan", 3)
        self.role_combo.addItem("Yönetici", 2)
        self.role_combo.addItem("Genel Müdür", 1)
        form.addRow("Rol:", self.role_combo)

        self.department_combo = QComboBox()
        self.department_combo.addItem("Yazılım", 1)
        self.department_combo.addItem("İK", 2)
        self.department_combo.addItem("Pazarlama", 3)
        form.addRow("Departman:", self.department_combo)

        layout.addLayout(form)

        # Kullanıcı Ekle Butonu
        add_btn = QPushButton("➕ Ekle")
        add_btn.clicked.connect(self.submit_user)
        layout.addWidget(add_btn)

        # Geri Dön Butonu
        back_btn = QPushButton("◀️ Geri")
        back_btn.clicked.connect(lambda: self.main_app.setCurrentWidget(self.main_app.dashboard))
        layout.addWidget(back_btn)

        self.role_combo.currentIndexChanged.connect(self.toggle_department_visibility)
        self.toggle_department_visibility()  # ilk seçimde departmanı kontrol et

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
