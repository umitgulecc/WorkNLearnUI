from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class EmployeeDashboardPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.user_data = main_app.current_user
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        full_name = self.user_data.get("full_name", "Bilinmiyor")
        welcome = QLabel(f"👋 Hoş geldiniz, {full_name}!")
        welcome.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(welcome)
        
        logout = self.add_button("Çıkış Yap", self.logout_user)
        self.layout.addWidget(logout)

        self.add_button("📝 Quiz Çöz", self.main_app.go_to_quiz)

        self.load_solved_quizzes()

    def add_button(self, text, callback):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #333333;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button
    
    def load_solved_quizzes(self):
        solved = self.main_app.api.get_solved_quizzes()

        if not solved["success"]:
            err = QLabel("❌ Çözdüğünüz quizler yüklenemedi.")
            err.setStyleSheet("color: red;")
            self.layout.addWidget(err)
            return

        if not solved["quizzes"]:
            empty = QLabel("🕳 Henüz çözülmüş quiz bulunmuyor.")
            empty.setStyleSheet("color: white;")
            self.layout.addWidget(empty)
            return

        title = QLabel("📊 Çözdüğünüz Quizler")
        title.setStyleSheet("font-size: 16px; color: white; margin-top: 20px;")
        self.layout.addWidget(title)

        for quiz in solved["quizzes"]:
            self.add_solved_quiz_row(quiz)

    def add_solved_quiz_row(self, quiz):
        row = QVBoxLayout()
        title = QLabel(f"{quiz['title']} (ID: {quiz['quiz_id']})")
        title.setStyleSheet("color: white; font-size: 13px;")

        review_btn = QPushButton("🔍 İncele")
        review_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #333;
                border-radius: 6px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #dddddd;
            }
        """)
        review_btn.clicked.connect(lambda: self.main_app.go_to_review_quiz(quiz["result_id"]))

        row.addWidget(title)
        row.addStretch()
        row.addWidget(review_btn)
        self.layout.addLayout(row)
        
    def logout_user(self):
        self.api.logout()
        self.main_app.go_to_login()
