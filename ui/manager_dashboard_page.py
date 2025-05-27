from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout
)
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

        # Karşılama
        full_name = self.user_data.get("full_name", "Bilinmiyor")
        welcome = QLabel(f"👋 Hoş geldiniz, {full_name}!")
        welcome.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(welcome)

        # Butonlar
        add_employee_btn = QPushButton("👤 Çalışan Ekle")
        add_employee_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #4CAF50; color: white; border-radius: 8px;")
        add_employee_btn.clicked.connect(self.open_add_employee_form)
        self.layout.addWidget(add_employee_btn)

        delete_employee_btn = QPushButton("👤 Çalışan Sil")
        delete_employee_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #eb2522; color: white; border-radius: 8px;")
        delete_employee_btn.clicked.connect(lambda: self.main_app.show_delete_employee_page())
        self.layout.addWidget(delete_employee_btn)

        logout_btn = QPushButton("Çıkış Yap")
        logout_btn.clicked.connect(self.logout_user)
        self.layout.addWidget(logout_btn)

        # Tablo başlık
        self.table_title = QLabel("👥 Takım Performansı")
        self.table_title.setStyleSheet("font-size: 16px; color: white; margin-top: 20px;")
        self.layout.addWidget(self.table_title)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Ad Soyad", "Seviye", "Ortalama Skor", "Toplam Skor", "Detay"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        self.load_team_summary()

    def load_team_summary(self):
        result = self.api.get_team_summary()

        if not result["success"]:
            QMessageBox.warning(self, "Hata", "❌ Takım verileri yüklenemedi.")
            return

        self.table.setRowCount(0)  # Tüm satırları temizle

        for member in result["members"]:
            self.add_team_member_row(member)

    def add_team_member_row(self, member):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(member["full_name"]))
        self.table.setItem(row, 1, QTableWidgetItem(str(member["level"])))
        self.table.setItem(row, 2, QTableWidgetItem(str(member["average_score"])))
        self.table.setItem(row, 3, QTableWidgetItem(str(member["total_score"])))

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
        self.table.setCellWidget(row, 4, detail_btn)

    def open_add_employee_form(self):
        from ui.add_employee_form_page import AddEmployeeForm
        self.form = AddEmployeeForm(self.main_app)  # ✅ API değil, main_app gönderiyoruz
        self.form.show()


    def logout_user(self):
        self.api.logout()
        self.main_app.go_to_login()

    def refresh_team_summary(self):
        # Sadece satırları temizle ve yeniden doldur
        self.load_team_summary()
