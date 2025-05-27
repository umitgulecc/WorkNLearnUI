from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class AddEmployeeForm(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("Yeni Çalışan Ekle")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ad Soyad")
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        
        self.department_input = QLineEdit()
        self.department_input.setPlaceholderText("Departman Adı")
        layout.addWidget(self.department_input)   
        
        
        self.submit_btn = QPushButton("✅ Kaydet")
        self.submit_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border-radius: 6px;")
        self.submit_btn.clicked.connect(self.register_employee)
        layout.addWidget(self.submit_btn)

    def register_employee(self):
        departments = self.api.get_departments()  # [{"id": 1, "name": "İnsan Kaynakları"}, ...]
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
                self.accept()
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

        # Harfleri değiştir
        for turkish, english in replacements.items():
            text = text.replace(turkish, english)

        # Tamamen büyük harf yap
        return text.upper()
