from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHeaderView, QFrame,
    QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class DeleteEmployeePage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.setup_ui()
        self.load_employees()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)
        self.setWindowTitle("Çalışan Sil")
        self.setFixedSize(800, 600)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(SPACING)
        self.layout.setContentsMargins(*MARGINS)

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
        title = QLabel("🗑️ Çalışan Sil")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title)

        # Back button
        back_btn = QPushButton("← Geri")
        back_btn.setFont(DEFAULT_FONT)
        back_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.close)
        header_layout.addWidget(back_btn)

        self.layout.addWidget(header_container)

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
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {COLORS['background']};
            }}
        """)
        table_layout.addWidget(self.table)

        self.layout.addWidget(table_container)

    def load_employees(self):
        users = self.api.get_users_by_department()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tam Adı", "Level", "Email", "Sil"])
        self.table.setRowCount(len(users))
        print("Çalışanlar:", users[0])
        
        for row, user in enumerate(users):
            # Create and style items
            id_item = QTableWidgetItem(str(user["id"]))
            name_item = QTableWidgetItem(user["full_name"])
            level_item = QTableWidgetItem(str(user["level_id"]))
            email_item = QTableWidgetItem(user["email"])

            # Set font for items
            id_item.setFont(DEFAULT_FONT)
            name_item.setFont(DEFAULT_FONT)
            level_item.setFont(DEFAULT_FONT)
            email_item.setFont(DEFAULT_FONT)

            # Add items to table
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, level_item)
            self.table.setItem(row, 3, email_item)

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
            delete_btn.clicked.connect(lambda checked, user_id=user["id"]: self.delete_user(user_id))
            self.table.setCellWidget(row, 4, delete_btn)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_user(self, user_id):
        result = self.api.delete_user_by_id(user_id)
        if result["success"]:
            QMessageBox.information(self, "Başarılı", result["detail"])
            self.load_employees()  # Refresh table
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
