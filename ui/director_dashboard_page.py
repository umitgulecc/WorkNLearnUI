from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class DirectorDashboardPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.user_data = main_app.current_user
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

        # Welcome message
        full_name = self.user_data.get("full_name", "Bilinmiyor")
        welcome = QLabel(f"👋 Hoş geldiniz, {full_name}!")
        welcome.setFont(TITLE_FONT)
        welcome.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(welcome)

        # Logout button
        logout_btn = QPushButton("🚪 Çıkış Yap")
        logout_btn.setFont(DEFAULT_FONT)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['error']};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                color: {COLORS['text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #FF9999;
                color: {COLORS['white']};
            }}
        """)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)

        layout.addWidget(header_container)

        # Info container
        info_container = QFrame()
        info_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(SPACING)

        # Info message
        info = QLabel("")
        info.setFont(DEFAULT_FONT)
        info.setStyleSheet(f"color: {COLORS['text']}; font-size: 14px;")
        info_layout.addWidget(info)

        layout.addWidget(info_container)

        # Actions container
        actions_container = QFrame()
        actions_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        actions_layout = QVBoxLayout(actions_container)
        actions_layout.setSpacing(SPACING)

        # Add user button
        add_user_btn = QPushButton("➕ Kullanıcı Ekle")
        add_user_btn.setFont(DEFAULT_FONT)
        add_user_btn.setStyleSheet(f"""
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
        add_user_btn.setCursor(Qt.PointingHandCursor)
        add_user_btn.clicked.connect(self.open_add_members_page)
        actions_layout.addWidget(add_user_btn)

        # Delete all users button
        delete_user_btn = QPushButton("🗑️ Kullanıcıları Sil")
        delete_user_btn.setFont(DEFAULT_FONT)
        delete_user_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['error']};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                color: {COLORS['text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #FF9999;
                color: {COLORS['white']};
            }}
        """)
        delete_user_btn.setCursor(Qt.PointingHandCursor)
        delete_user_btn.clicked.connect(self.open_delete_all_members_page)
        actions_layout.addWidget(delete_user_btn)

        layout.addWidget(actions_container)

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
