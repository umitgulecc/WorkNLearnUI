from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QFrame, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class EmployeeDashboardPage(QWidget):
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
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(SPACING)
        self.layout.setContentsMargins(*MARGINS)
        self.layout.setAlignment(Qt.AlignTop)

        # Create header container
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
        logout = QPushButton("Çıkış Yap")
        logout.setFont(DEFAULT_FONT)
        logout.setStyleSheet(BUTTON_STYLE)
        logout.setCursor(Qt.PointingHandCursor)
        logout.clicked.connect(self.logout_user)
        header_layout.addWidget(logout)
        
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
        actions_layout = QVBoxLayout(actions_container)
        actions_layout.setSpacing(SPACING)

        # Action buttons
        quiz_btn = QPushButton("📝 Quiz Çöz")
        quiz_btn.setFont(DEFAULT_FONT)
        quiz_btn.setStyleSheet(BUTTON_STYLE)
        quiz_btn.setCursor(Qt.PointingHandCursor)
        quiz_btn.clicked.connect(self.main_app.go_to_quiz)
        actions_layout.addWidget(quiz_btn)

        stats_btn = QPushButton("📈 İstatistiklerim")
        stats_btn.setFont(DEFAULT_FONT)
        stats_btn.setStyleSheet(BUTTON_STYLE)
        stats_btn.setCursor(Qt.PointingHandCursor)
        stats_btn.clicked.connect(self.main_app.go_to_employee_stats)
        actions_layout.addWidget(stats_btn)

        self.layout.addWidget(actions_container)

        # Load solved quizzes
        self.load_solved_quizzes()

    def load_solved_quizzes(self):
        solved = self.main_app.api.get_solved_quizzes()
        print("Çözülen quizler:", solved)

        # Remove old table if exists
        if hasattr(self, "table_container"):
            self.layout.removeWidget(self.table_container)
            self.table_container.deleteLater()

        # Create table container
        self.table_container = QFrame()
        self.table_container.setStyleSheet(f"""
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
        table_layout = QVBoxLayout(self.table_container)

        # Table title
        table_title = QLabel("Çözülen Quizler")
        table_title.setFont(TITLE_FONT)
        table_title.setStyleSheet(TITLE_STYLE)
        table_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setFont(DEFAULT_FONT)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Quiz Başlığı", "İncele"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {COLORS['background']};
            }}
        """)
        table_layout.addWidget(self.table)

        if not solved["success"]:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("❌ Quizler yüklenemedi."))
            return

        quizzes = solved["quizzes"]

        if not quizzes:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("🕳 Henüz çözülmüş quiz bulunmuyor."))
            return

        self.table.setRowCount(len(quizzes))
        for i, quiz in enumerate(quizzes):
            title_item = QTableWidgetItem(quiz["title"])
            title_item.setFont(DEFAULT_FONT)
            self.table.setItem(i, 0, title_item)

            review_btn = QPushButton("🔍 İncele")
            review_btn.setFont(DEFAULT_FONT)
            review_btn.setStyleSheet(BUTTON_STYLE)
            review_btn.setCursor(Qt.PointingHandCursor)
            review_btn.clicked.connect(lambda _, rid=quiz["result_id"]: self.main_app.go_to_review_quiz(rid))
            self.table.setCellWidget(i, 1, review_btn)

        self.layout.addWidget(self.table_container)

    def logout_user(self):
        self.api.logout()
        self.main_app.go_to_login()
