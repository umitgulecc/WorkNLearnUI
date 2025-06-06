# main.py
from PySide6.QtWidgets import QApplication, QStackedWidget
from ui.login_page import LoginPage
from ui.quiz_page import QuizPage
from api_client import APIClient
from ui.result_page import ResultsPage
from ui.solve_quiz_page import SolveQuizPage
from ui.solve_quiz_page_reading import SolveQuizPageReading
from ui.review_quiz_page import ReviewQuizPage

import sys

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WORK-n-LEARN")
        self.setFixedSize(900, 800)

        self.api = APIClient("http://127.0.0.1:8000")  # ⬅ global api client
        self.current_user = None

        self.login_page = LoginPage(self)
        self.addWidget(self.login_page)
        self.setCurrentWidget(self.login_page)

    def show_role_dashboard(self, user_data):
        self.current_user = user_data
        role_id = user_data.get("role_id")
        print("Rol ID:", role_id)

        if role_id == 3:  # 🎓 Çalışan
            from ui.employee_dashboard_page import EmployeeDashboardPage
            self.dashboard = EmployeeDashboardPage(self)

        elif role_id == 2:  # 🧑‍💼 Müdür
            from ui.manager_dashboard_page import ManagerDashboardPage
            self.manager_dashboard_page = ManagerDashboardPage(self)  # ✅ ekledik
            self.dashboard = self.manager_dashboard_page              # ✅ eskisi korunuyor

        elif role_id == 1:  # 👑 Genel Müdür
            from ui.director_dashboard_page import DirectorDashboardPage
            self.director_dashboard_page = DirectorDashboardPage(self)
            self.dashboard = self.director_dashboard_page

        else:
            from PySide6.QtWidgets import QLabel
            self.dashboard = QLabel("⚠️ Geçersiz rol.")

        self.addWidget(self.dashboard)
        self.setCurrentWidget(self.dashboard)




    def go_to_quiz(self):
        self.quiz_page = QuizPage(self)
        self.addWidget(self.quiz_page)
        self.setCurrentWidget(self.quiz_page)

    def go_to_solve_quiz(self, quiz):
        if quiz["skill_id"] in[1,3]:
            self.solve_quiz_page = SolveQuizPage(self, quiz["id"])
            self.addWidget(self.solve_quiz_page)
            self.setCurrentWidget(self.solve_quiz_page)
        else:
            self.solve_quiz_page_reading = SolveQuizPageReading(self, quiz["id"])
            self.addWidget(self.solve_quiz_page_reading)
            self.setCurrentWidget(self.solve_quiz_page_reading)
    

    def go_to_review_quiz(self, result_id, user_id=None):
        from ui.review_quiz_page import ReviewQuizPage
        self.review_page = ReviewQuizPage(self, result_id, user_id)
        self.addWidget(self.review_page)
        self.setCurrentWidget(self.review_page)


    def go_to_results(self):
        self.results_page = ResultsPage(self)
        self.addWidget(self.results_page)
        self.setCurrentWidget(self.results_page)

    def go_to_team_member_details(self, user_id):
        from ui.team_member_details_page import TeamMemberDetailsPage
        self.details_page = TeamMemberDetailsPage(self, user_id)
        self.addWidget(self.details_page)
        self.setCurrentWidget(self.details_page)

    def go_to_login(self):
        self.current_user = None
        self.login_page = LoginPage(self)
        self.addWidget(self.login_page)
        self.setCurrentWidget(self.login_page)

    
    def show_delete_employee_page(self):
        from ui.delete_employee_page import DeleteEmployeePage
        self.delete_employee_page = DeleteEmployeePage(self)
        self.delete_employee_page.show()

    def go_to_employee_stats(self):
        from ui.employee_stats_page import EmployeeStatsPage
        self.stats_page = EmployeeStatsPage(self)
        self.addWidget(self.stats_page)
        self.setCurrentWidget(self.stats_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
