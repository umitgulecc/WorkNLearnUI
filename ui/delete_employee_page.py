from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView

class DeleteEmployeePage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.setWindowTitle("Çalışan Sil")
        self.setFixedSize(600, 400)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.load_employees()

    def load_employees(self):
        users = self.api.get_users_by_department()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tam Adı", "Level", "Email", "Sil"])
        self.table.setRowCount(len(users))
        print("Çalışanlar:", users[0])
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(user["full_name"]))  # Ad
            self.table.setItem(row, 2, QTableWidgetItem(str(user["level_id"])))
            self.table.setItem(row, 3, QTableWidgetItem(user["email"]))

            delete_btn = QPushButton("Sil")
            delete_btn.setStyleSheet("background-color: red; color: white; padding: 5px;")
            delete_btn.clicked.connect(lambda checked, user_id=user["id"]: self.delete_user(user_id))
            self.table.setCellWidget(row, 4, delete_btn)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_user(self, user_id):
        result = self.api.delete_user_by_id(user_id)
        if result["success"]:
            QMessageBox.information(self, "Silindi", result["detail"])
            self.load_employees()  # tabloyu yenile
        else:
            QMessageBox.warning(self, "Hata", result["detail"])

    
    def closeEvent(self, event):
        print("❌ DeleteEmployeePage kapandı")
        if hasattr(self.main_app, "manager_dashboard_page"):
            print("✅ manager_dashboard_page bulundu, refresh çağrılıyor")
            self.main_app.manager_dashboard_page.refresh_team_summary()
        else:
            print("❌ manager_dashboard_page bulunamadı")
        super().closeEvent(event)
