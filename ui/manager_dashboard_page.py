from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QFrame, QHeaderView
)
from PySide6.QtCore import Qt
from ui.add_employee_form_page import AddEmployeeForm
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class ManagerDashboardPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user_data = main_app.current_user
        self.api = main_app.api
        self.setup_ui()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(SPACING)
        self.layout.setContentsMargins(*MARGINS)
        self.layout.setAlignment(Qt.AlignTop)

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

        # Logout button in header
        logout_btn = QPushButton("Çıkış Yap")
        logout_btn.setFont(DEFAULT_FONT)
        logout_btn.setStyleSheet(BUTTON_STYLE)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout_user)
        header_layout.addWidget(logout_btn)

        self.layout.addWidget(header_container)

        # Actions container
        actions_container = QFrame()
        actions_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setSpacing(SPACING)

        # Add employee button
        add_employee_btn = QPushButton("👤 Çalışan Ekle")
        add_employee_btn.setFont(DEFAULT_FONT)
        add_employee_btn.setStyleSheet(f"""
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
        add_employee_btn.setCursor(Qt.PointingHandCursor)
        add_employee_btn.clicked.connect(self.open_add_employee_form)
        actions_layout.addWidget(add_employee_btn)

        # Delete employee button
        delete_employee_btn = QPushButton("👤 Çalışan Sil")
        delete_employee_btn.setFont(DEFAULT_FONT)
        delete_employee_btn.setStyleSheet(f"""
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
        delete_employee_btn.setCursor(Qt.PointingHandCursor)
        delete_employee_btn.clicked.connect(lambda: self.main_app.show_delete_employee_page())
        actions_layout.addWidget(delete_employee_btn)

        self.layout.addWidget(actions_container)

        # Team performance container
        team_container = QFrame()
        team_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
            QTableWidget {{
                background-color: {COLORS['white']};
                border: none;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['primary']};
                padding: 10px;
                border: none;
                font-weight: bold;
                color: {COLORS['text']};
            }}
        """)
        team_layout = QVBoxLayout(team_container)
        team_layout.setSpacing(SPACING)

        # Table title
        self.table_title = QLabel("👥 mansı")
        self.table_title.setFont(TITLE_FONT)
        self.table_title.setStyleSheet(TITLE_STYLE)
        team_layout.addWidget(self.table_title)

        # Team performance table
        self.table = QTableWidget()
        self.table.setFont(DEFAULT_FONT)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Ad Soyad", "Seviye", "Ortalama Skor", "Toplam Skor", "Detay"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {COLORS['background']};
            }}
        """)
        team_layout.addWidget(self.table)

        self.layout.addWidget(team_container)
        self.load_team_summary()

    def load_team_summary(self):
        result = self.api.get_team_summary()

        if not result["success"]:
            QMessageBox.warning(self, "Hata", "❌ Takım verileri yüklenemedi.")
            return

        self.table.setRowCount(0)  # Clear all rows

        for member in result["members"]:
            self.add_team_member_row(member)

    def add_team_member_row(self, member):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Add member data with proper font
        for col, value in enumerate([
            member["full_name"],
            str(member["level"]),
            str(member["average_score"]),
            str(member["total_score"])
        ]):
            item = QTableWidgetItem(value)
            item.setFont(DEFAULT_FONT)
            self.table.setItem(row, col, item)

        # Detail button
        detail_btn = QPushButton("🔍 Detaylar")
        detail_btn.setFont(DEFAULT_FONT)
        detail_btn.setStyleSheet(BUTTON_STYLE)
        detail_btn.setCursor(Qt.PointingHandCursor)
        detail_btn.clicked.connect(lambda: self.main_app.go_to_team_member_details(member["user_id"]))
        self.table.setCellWidget(row, 4, detail_btn)

    def open_add_employee_form(self):
        self.form = AddEmployeeForm(self.main_app)
        self.form.show()

    def logout_user(self):
        self.api.logout()
        self.main_app.go_to_login()

    def refresh_team_summary(self):
        self.load_team_summary()
