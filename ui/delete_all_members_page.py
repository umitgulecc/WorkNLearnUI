from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QFrame, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class DeleteAllMembersPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.setup_ui()
        self.load_users()

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
        title = QLabel("🗑 Kullanıcı Silme Paneli")
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

        # Table container
        table_container = QFrame()
        table_container.setStyleSheet(f"""
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
                padding: 10px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['primary']};
                padding: 10px;
                border: none;
                font-weight: bold;
                color: {COLORS['text']};
            }}
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setSpacing(SPACING)

        # Table
        self.table = QTableWidget()
        self.table.setFont(DEFAULT_FONT)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-Posta", "Rol", "İşlem"])
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {COLORS['background']};
            }}
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_container)

    def load_users(self):
        self.table.setRowCount(0)
        users = self.api.get_all_users()
        for row_index, user in enumerate(users):
            self.table.insertRow(row_index)

            # Create and style items
            id_item = QTableWidgetItem(str(user["id"]))
            name_item = QTableWidgetItem(user["full_name"])
            email_item = QTableWidgetItem(user["email"])
            role_item = QTableWidgetItem(self.role_label(user["role_id"]))

            # Set font for items
            id_item.setFont(DEFAULT_FONT)
            name_item.setFont(DEFAULT_FONT)
            email_item.setFont(DEFAULT_FONT)
            role_item.setFont(DEFAULT_FONT)

            # Add items to table
            self.table.setItem(row_index, 0, id_item)
            self.table.setItem(row_index, 1, name_item)
            self.table.setItem(row_index, 2, email_item)
            self.table.setItem(row_index, 3, role_item)

            # Delete button
            delete_btn = QPushButton("🗑️ Sil")
            delete_btn.setFont(DEFAULT_FONT)
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['error']};
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    color: {COLORS['text']};
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #FF9999;
                    color: {COLORS['white']};
                }}
            """)
            delete_btn.setCursor(Qt.PointingHandCursor)
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
