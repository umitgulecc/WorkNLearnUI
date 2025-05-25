from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class QuizPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user = main_app.current_user
        self.api = main_app.api
        self.setup_ui()
        self.load_quizzes()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        title = QLabel("📝 Erişebileceğin Quizler")
        title.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(title)

        self.quiz_container = QVBoxLayout()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.quiz_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        back_button = QPushButton("← Geri")
        back_button.clicked.connect(lambda: self.main_app.show_dashboard(self.user))
        self.layout.addWidget(back_button)

    def load_quizzes(self):
        result = self.api.get_available_quizzes()
        print("Quiz çekme sonucu:", result)

        if result["success"]:
            for quiz in result["quizzes"]:
                self.add_quiz_item(quiz)
        else:
            err = QLabel("❌ Quiz bulunamadı veya erişim hatası.")
            err.setStyleSheet("color: red;")
            self.quiz_container.addWidget(err)

    def add_quiz_item(self, quiz):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        hbox = QHBoxLayout(frame)

        title = QLabel(f"{quiz['title']} (Seviye {quiz['level_id']})")
        title.setStyleSheet("font-size: 14px; color: black;")

        start_btn = QPushButton("🚀 Başla")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #66a6ff;
                color: white;
                padding: 6px 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #558be0;
            }
        """)
        start_btn.clicked.connect(lambda: self.main_app.go_to_solve_quiz(quiz["id"]))

        hbox.addWidget(title)
        hbox.addStretch()
        hbox.addWidget(start_btn)

        self.quiz_container.addWidget(frame)
