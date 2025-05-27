from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class DeleteAllMembersPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.setStyleSheet(APP_STYLE)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("🗑 Kullanıcı Silme Paneli")
        title.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(title)

        # Tablo: Kullanıcıları listele
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-Posta", "Rol", "İşlem"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Geri Dön Butonu
        back_btn = QPushButton("◀️ Geri")
        back_btn.clicked.connect(lambda: self.main_app.setCurrentWidget(self.main_app.dashboard))
        layout.addWidget(back_btn)

        self.load_users()

    def load_users(self):
        self.table.setRowCount(0)
        users = self.api.get_all_users()
        for row_index, user in enumerate(users):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(str(user["id"])))
            self.table.setItem(row_index, 1, QTableWidgetItem(user["full_name"]))
            self.table.setItem(row_index, 2, QTableWidgetItem(user["email"]))
            self.table.setItem(row_index, 3, QTableWidgetItem(self.role_label(user["role_id"])))

            # Sil Butonu
            delete_btn = QPushButton("🗑 Sil")
            delete_btn.clicked.connect(lambda _, uid=user["id"]: self.delete_user(uid))
            self.table.setCellWidget(row_index, 4, delete_btn)

    def delete_user(self, user_id):
        if user_id == self.main_app.current_user["id"]:
            QMessageBox.warning(self, "Uyarı", "Kendi hesabınızı silemezsiniz.")
            return

        confirm = QMessageBox.question(
            self,
            "Emin misiniz?",
            f"Kullanıcı ID {user_id} silinsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            result = self.api.delete_user_by_id(user_id)
            if result["success"]:
                QMessageBox.information(self, "Başarılı", "Kullanıcı silindi.")
                self.load_users()
            else:
                QMessageBox.critical(self, "Hata", f"Kullanıcı silinemedi:\n{result['detail']}")

    def role_label(self, role_id):
        return {
            1: "Genel Müdür",
            2: "Yönetici",
            3: "Çalışan"
        }.get(role_id, "Bilinmiyor")
