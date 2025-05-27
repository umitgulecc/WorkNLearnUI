from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class TeamMemberDetailsPage(QWidget):
    def __init__(self, main_app, user_id):
        super().__init__()
        self.main_app = main_app
        self.user_id = user_id
        self.api = main_app.api

        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        title = QLabel("👤 Çalışan Quiz Sonuçları")
        title.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(title)

        self.load_user_results()

        back_btn = QPushButton("← Geri")
        back_btn.clicked.connect(self.go_back)
        self.layout.addWidget(back_btn)

    def load_user_results(self):
        result = self.api.get_user_results(self.user_id)
        print("Kullanıcı sonuçları:", result)
        if not result["success"]:
            err = QLabel("❌ Quiz verisi alınamadı.")
            err.setStyleSheet("color: red;")
            self.layout.addWidget(err)
            return

        quizzes = result["quizzes"]
        if not quizzes:
            empty = QLabel("🕳 Bu kullanıcı henüz quiz çözmemiş.")
            empty.setStyleSheet("color: white;")
            self.layout.addWidget(empty)
            return

        for quiz in quizzes:
            row = QVBoxLayout()
            title = QLabel(f"{quiz['quiz_title']} | Skor: {quiz['score']} | Tarih: {quiz['taken_at']}")
            title.setStyleSheet("color: white; font-size: 14px;")

            detail_btn = QPushButton("🔍 İncele")
            print("member detayları:", self.user_id, quiz['result_id'])
            detail_btn.clicked.connect(lambda _, rid=quiz['result_id']: self.main_app.go_to_review_quiz(rid, self.user_id))

            row.addWidget(title)
            row.addWidget(detail_btn)
            self.layout.addLayout(row)

    def go_back(self):
        from ui.manager_dashboard_page import ManagerDashboardPage
        self.main_app.dashboard = ManagerDashboardPage(self.main_app)
        self.main_app.addWidget(self.main_app.dashboard)
        self.main_app.setCurrentWidget(self.main_app.dashboard)