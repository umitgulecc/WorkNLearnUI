from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
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
        print("Çözülen quizler:", solved)

        # Önce varsa eski tabloyu temizle
        if hasattr(self, "table"):
            self.layout.removeWidget(self.table)
            self.table.deleteLater()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Quiz Başlığı", "İncele"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

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
            self.table.setItem(i, 0, QTableWidgetItem(quiz["title"]))

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
            review_btn.clicked.connect(lambda _, rid=quiz["result_id"]: self.main_app.go_to_review_quiz(rid))
            self.table.setCellWidget(i, 1, review_btn)

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
