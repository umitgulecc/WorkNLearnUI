from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class ResultsPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.user = main_app.current_user
        self.api = main_app.api

        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        title = QLabel("📊 Sonuçlarım" if self.user["role_id"] == 3 else "👥 Takım Sonuçları")
        title.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5 if self.user["role_id"] == 3 else 6)
        self.layout.addWidget(self.table)

        if self.user["role_id"] == 3:
            self.load_personal_results()
        elif self.user["role_id"] == 2:
            self.load_team_summary()

    def load_personal_results(self):
        result = self.api.get_solved_quizzes()
        if not result["success"]:
            self.table.setRowCount(0)
            return

        quizzes = result["quizzes"]
        self.table.setHorizontalHeaderLabels(["Quiz", "Seviye", "Skor", "Tarih", "İncele"])
        self.table.setRowCount(len(quizzes))

        for row, quiz in enumerate(quizzes):
            self.table.setItem(row, 0, QTableWidgetItem(quiz["title"]))
            self.table.setItem(row, 1, QTableWidgetItem(f"Seviye {quiz['level_id']}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(quiz.get("score", "-"))))
            self.table.setItem(row, 3, QTableWidgetItem(quiz.get("taken_at", "-")))

            btn = QPushButton("🔍")
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
            self.table.setItem(row, 0, QTableWidgetItem(member["full_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(member["level"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(member["total_quizzes"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(member["average_score"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(member["total_score"])))

            btn = QPushButton("Detay")
            btn.clicked.connect(lambda _, uid=member["user_id"]: self.main_app.go_to_team_member_details(uid))
            self.table.setCellWidget(row, 5, btn)
