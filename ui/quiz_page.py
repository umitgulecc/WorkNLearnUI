from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class QuizPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user = main_app.current_user
        self.api = main_app.api
        self.setup_ui()
        self.load_quizzes()

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
        title = QLabel("📝 Erişebileceğin Quizler")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title)

        # Back button
        back_button = QPushButton("← Geri")
        back_button.setFont(DEFAULT_FONT)
        back_button.setStyleSheet(BUTTON_STYLE)
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(lambda: self.main_app.show_role_dashboard(self.user))
        header_layout.addWidget(back_button)

        self.layout.addWidget(header_container)

        # Quiz list container
        quiz_list_container = QFrame()
        quiz_list_container.setStyleSheet(f"""
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
        quiz_list_layout = QVBoxLayout(quiz_list_container)
        quiz_list_layout.setSpacing(SPACING)

        # Scroll area for quizzes
        self.quiz_container = QVBoxLayout()
        self.quiz_container.setSpacing(SPACING)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.quiz_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        quiz_list_layout.addWidget(scroll_area)

        self.layout.addWidget(quiz_list_container)

    def load_quizzes(self):
        result = self.api.get_available_quizzes()
        if result["success"]:
            for quiz in result["quizzes"]:
                self.add_quiz_item(quiz)
        else:
            err = QLabel("❌ Quiz bulunamadı veya erişim hatası.")
            err.setFont(DEFAULT_FONT)
            err.setStyleSheet(f"color: {COLORS['error']};")
            self.quiz_container.addWidget(err)

    def add_quiz_item(self, quiz):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        hbox = QHBoxLayout(frame)
        hbox.setSpacing(SPACING)

        # Quiz info
        info_layout = QVBoxLayout()
        
        title = QLabel(f"{quiz['title']}")
        title.setFont(DEFAULT_FONT)
        title.setStyleSheet(f"color: {COLORS['text']}; font-weight: bold;")
        
        level = QLabel(f"Seviye {quiz['level_id']}")
        level.setFont(DEFAULT_FONT)
        level.setStyleSheet(f"color: {COLORS['text']};")
        
        info_layout.addWidget(title)
        info_layout.addWidget(level)
        
        hbox.addLayout(info_layout)
        hbox.addStretch()

        # Start button
        start_btn = QPushButton("🚀 Başla")
        start_btn.setFont(DEFAULT_FONT)
        start_btn.setStyleSheet(BUTTON_STYLE)
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.clicked.connect(lambda: self.main_app.go_to_solve_quiz(quiz))
        hbox.addWidget(start_btn)

        self.quiz_container.addWidget(frame)
