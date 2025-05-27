from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class TeamMemberDetailsPage(QWidget):
    def __init__(self, main_app, user_id):
        super().__init__()
        self.main_app = main_app
        self.user_id = user_id
        self.api = main_app.api
        self.setup_ui()
        self.load_user_results()

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
        title = QLabel("👤 Çalışan Quiz Sonuçları")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title)

        # Back button
        back_btn = QPushButton("← Geri")
        back_btn.setFont(DEFAULT_FONT)
        back_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        self.layout.addWidget(header_container)

        # Results container
        results_container = QFrame()
        results_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {COLORS['background']};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['primary']};
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        results_layout = QVBoxLayout(results_container)
        results_layout.setSpacing(SPACING)

        # Scroll area for results
        scroll_widget = QWidget()
        self.results_layout = QVBoxLayout(scroll_widget)
        self.results_layout.setSpacing(SPACING)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        results_layout.addWidget(scroll_area)

        self.layout.addWidget(results_container)

    def load_user_results(self):
        result = self.api.get_user_results(self.user_id)
        print("Kullanıcı sonuçları:", result)
        if not result["success"]:
            err = QLabel("❌ Quiz verisi alınamadı.")
            err.setFont(DEFAULT_FONT)
            err.setStyleSheet(f"color: {COLORS['error']};")
            self.results_layout.addWidget(err)
            return

        quizzes = result["quizzes"]
        if not quizzes:
            empty = QLabel("🕳 Bu kullanıcı henüz quiz çözmemiş.")
            empty.setFont(DEFAULT_FONT)
            empty.setStyleSheet(f"color: {COLORS['text']};")
            self.results_layout.addWidget(empty)
            return

        for quiz in quizzes:
            # Quiz result container
            quiz_frame = QFrame()
            quiz_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['background']};
                    border-radius: 8px;
                    padding: 15px;
                }}
            """)
            quiz_layout = QHBoxLayout(quiz_frame)
            quiz_layout.setSpacing(SPACING)

            # Quiz info
            info_layout = QVBoxLayout()
            
            title = QLabel(f"📝 {quiz['quiz_title']}")
            title.setFont(DEFAULT_FONT)
            title.setStyleSheet(f"color: {COLORS['text']}; font-weight: bold;")
            
            stats = QLabel(f"📊 Skor: {quiz['score']} | 🕒 {quiz['taken_at']}")
            stats.setFont(DEFAULT_FONT)
            stats.setStyleSheet(f"color: {COLORS['text']};")
            
            info_layout.addWidget(title)
            info_layout.addWidget(stats)
            
            quiz_layout.addLayout(info_layout)
            quiz_layout.addStretch()

            # Detail button
            detail_btn = QPushButton("🔍 İncele")
            detail_btn.setFont(DEFAULT_FONT)
            detail_btn.setStyleSheet(BUTTON_STYLE)
            detail_btn.setCursor(Qt.PointingHandCursor)
            detail_btn.clicked.connect(lambda _, rid=quiz['result_id']: self.main_app.go_to_review_quiz(rid, self.user_id))
            quiz_layout.addWidget(detail_btn)

            self.results_layout.addWidget(quiz_frame)

    def go_back(self):
        from ui.manager_dashboard_page import ManagerDashboardPage
        self.main_app.dashboard = ManagerDashboardPage(self.main_app)
        self.main_app.addWidget(self.main_app.dashboard)
        self.main_app.setCurrentWidget(self.main_app.dashboard)