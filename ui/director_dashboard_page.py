from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class DirectorDashboardPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.user_data = main_app.current_user
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        full_name = self.user_data.get("full_name", "Bilinmiyor")
        welcome = QLabel(f"👋 Hoş geldiniz, {full_name}!")
        welcome.setStyleSheet("font-size: 20px; color: white;")
        layout.addWidget(welcome)

        info = QLabel("🔧 Genel Müdür paneli henüz geliştirilme aşamasındadır.")
        info.setStyleSheet("color: white; font-size: 14px; margin-top: 20px;")
        layout.addWidget(info)

        # 🚪 Çıkış Yap Butonu
        logout_btn = QPushButton("🚪 Çıkış Yap")
        logout_btn.setStyleSheet("margin-top: 10px; padding: 10px; font-size: 14px; background-color: #d9534f; color: white;")
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)

        # ➕ Kullanıcı Ekle Butonu
        add_user_btn = QPushButton("➕ Kullanıcı Ekle")
        add_user_btn.setStyleSheet("margin-top: 30px; padding: 10px; font-size: 14px;")
        add_user_btn.clicked.connect(self.open_add_members_page)
        layout.addWidget(add_user_btn)

        # 🗑️ Tüm Kullanıcıları Sil Butonu
        delete_user_btn = QPushButton("🗑️ Kullanıcıları Sil")
        delete_user_btn.setStyleSheet("margin-top: 10px; padding: 10px; font-size: 14px;")
        delete_user_btn.clicked.connect(self.open_delete_all_members_page)
        layout.addWidget(delete_user_btn)

    def open_add_members_page(self):
        from ui.add_members_page import AddMembersPage
        page = AddMembersPage(self.main_app)
        self.main_app.addWidget(page)
        self.main_app.setCurrentWidget(page)


    def open_delete_all_members_page(self):
        from ui.delete_all_members_page import DeleteAllMembersPage
        page = DeleteAllMembersPage(self.main_app)
        self.main_app.addWidget(page)
        self.main_app.setCurrentWidget(page)


    def handle_logout(self):
        print("🚪 Kullanıcı çıkış yaptı.")
        self.api.logout()
        self.main_app.go_to_login()
