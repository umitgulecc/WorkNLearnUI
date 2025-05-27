from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from ui.add_employee_form_page import AddEmployeeForm
from utils.style import APP_STYLE

class ManagerDashboardPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user_data = main_app.current_user
        self.api = main_app.api
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        full_name = self.user_data.get("full_name", "Bilinmiyor")
        welcome = QLabel(f"👋 Hoş geldiniz, {full_name}!")
        welcome.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(welcome)
        
        # "Çalışan Ekle" butonu
        add_employee_btn = QPushButton("👤 Çalışan Ekle")
        add_employee_btn.setStyleSheet(
            "padding: 10px; font-size: 14px; background-color: #4CAF50; color: white; border-radius: 8px;"
        )
        add_employee_btn.clicked.connect(self.open_add_employee_form)
        self.layout.addWidget(add_employee_btn)

        logout_btn =QPushButton("Çıkış Yap")
        logout_btn.clicked.connect(self.logout_user)
        self.layout.addWidget(logout_btn)
        
        self.load_team_summary()

    def load_team_summary(self):
        result = self.main_app.api.get_team_summary()

        if not result["success"]:
            err = QLabel("❌ Takım verileri yüklenemedi.")
            err.setStyleSheet("color: red;")
            self.layout.addWidget(err)
            return

        if not result["members"]:
            empty = QLabel("🕳 Takımda kayıtlı çalışan bulunamadı.")
            empty.setStyleSheet("color: white;")
            self.layout.addWidget(empty)
            return

        title = QLabel("👥 Takım Performansı")
        title.setStyleSheet("font-size: 16px; color: white; margin-top: 20px;")
        self.layout.addWidget(title)

        for member in result["members"]:
            self.add_team_member_row(member)

    def add_team_member_row(self, member):
        row_layout = QHBoxLayout()

        info = QLabel(f"{member['full_name']} | {member['level']} | Ortalama: {member['average_score']} | Toplam: {member['total_score']}")
        info.setStyleSheet("color: white; font-size: 13px;")

        detail_btn = QPushButton("🔍 Detaylar")
        detail_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #333;
                border-radius: 6px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #dddddd;
            }
        """)
        detail_btn.clicked.connect(lambda: self.main_app.go_to_team_member_details(member["user_id"]))

        row_layout.addWidget(info)
        row_layout.addStretch()
        row_layout.addWidget(detail_btn)
        self.layout.addLayout(row_layout)
        
        
        
    def open_add_employee_form(self):
        self.form = AddEmployeeForm(self.main_app.api)
        self.form.exec()
            
    def logout_user(self):
        self.api.logout()
        self.main_app.go_to_login()