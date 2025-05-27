from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QFrame,
    QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class ResultsPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user = main_app.current_user
        self.api = main_app.api
        self.setup_ui()

        if self.user["role_id"] == 3:
            self.load_personal_results()
        elif self.user["role_id"] == 2:
            self.load_team_summary()

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

        # Title
        title = QLabel("📊 Sonuçlarım" if self.user["role_id"] == 3 else "👥 Takım Sonuçları")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title)

        # Back button
        back_btn = QPushButton("← Geri")
        back_btn.setFont(DEFAULT_FONT)
        back_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.main_app.show_role_dashboard(self.user))
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
        self.table.setColumnCount(5 if self.user["role_id"] == 3 else 6)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {COLORS['background']};
            }}
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.table)

        self.layout.addWidget(table_container)

    def load_personal_results(self):
        result = self.api.get_solved_quizzes()
        if not result["success"]:
            self.table.setRowCount(0)
            return

        quizzes = result["quizzes"]
        self.table.setHorizontalHeaderLabels(["Quiz", "Seviye", "Skor", "Tarih", "İncele"])
        self.table.setRowCount(len(quizzes))

        for row, quiz in enumerate(quizzes):
            # Create and style items
            title_item = QTableWidgetItem(quiz["title"])
            level_item = QTableWidgetItem(f"Seviye {quiz['level_id']}")
            score_item = QTableWidgetItem(str(quiz.get("score", "-")))
            date_item = QTableWidgetItem(quiz.get("taken_at", "-"))

            # Set font for items
            title_item.setFont(DEFAULT_FONT)
            level_item.setFont(DEFAULT_FONT)
            score_item.setFont(DEFAULT_FONT)
            date_item.setFont(DEFAULT_FONT)

            # Add items to table
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, level_item)
            self.table.setItem(row, 2, score_item)
            self.table.setItem(row, 3, date_item)

            # Review button
            btn = QPushButton("🔍 İncele")
            btn.setFont(DEFAULT_FONT)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, rid=quiz["result_id"]: self.main_app.go_to_review_quiz(rid))
            self.table.setCellWidget(row, 4, btn)

    def load_team_summary(self):
        result = self.api.get_team_summary()
        if not result["success"]:
            self.table.setRowCount(0)
            return

        members = result["members"]
        self.table.setHorizontalHeaderLabels(["Ad", "Seviye", "Çözüm Sayısı", "Ortalama", "Toplam Skor", ""])
        self.table.setRowCount(len(members))

        for row, member in enumerate(members):
            # Create and style items
            name_item = QTableWidgetItem(member["full_name"])
            level_item = QTableWidgetItem(member["level"])
            quiz_count_item = QTableWidgetItem(str(member["total_quizzes"]))
            avg_score_item = QTableWidgetItem(str(member["average_score"]))
            total_score_item = QTableWidgetItem(str(member["total_score"]))

            # Set font for items
            name_item.setFont(DEFAULT_FONT)
            level_item.setFont(DEFAULT_FONT)
            quiz_count_item.setFont(DEFAULT_FONT)
            avg_score_item.setFont(DEFAULT_FONT)
            total_score_item.setFont(DEFAULT_FONT)

            # Add items to table
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, level_item)
            self.table.setItem(row, 2, quiz_count_item)
            self.table.setItem(row, 3, avg_score_item)
            self.table.setItem(row, 4, total_score_item)

            # Detail button
            btn = QPushButton("🔍 Detay")
            btn.setFont(DEFAULT_FONT)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, uid=member["user_id"]: self.main_app.go_to_team_member_details(uid))
            self.table.setCellWidget(row, 5, btn)
