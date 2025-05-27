from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class ReviewQuizPage(QWidget):
    def __init__(self, main_app, result_id, user_id=None): 
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.result_id = result_id
        self.user_id = user_id or main_app.current_user["id"]  # 👈 eğer None ise current_user.id

        self.setup_ui()
        self.load_review()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        title = QLabel("📋 Quiz Çözüm İncelemesi")
        title.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(title)

        self.review_container = QVBoxLayout()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.review_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        back = QLabel('<a href="#">← Geri</a>')
        back.setStyleSheet("color: white; margin-top: 20px;")
        back.setOpenExternalLinks(False)

        # Eğer detay bakılan kişi ile current_user aynıysa → çalışan kendi verisine bakıyor
        if self.user_id == self.main_app.current_user["id"]:
            back.linkActivated.connect(lambda _: self.main_app.show_role_dashboard(self.main_app.current_user))
        else:
            back.linkActivated.connect(lambda _: self.main_app.go_to_team_member_details(self.user_id))
            # 👆 Bu fonksiyon müdürün dashboarduna geri döner

        self.layout.addWidget(back)

    def load_review(self):
        result = self.api.get_quiz_review(self.result_id)
        if not result["success"]:
            err = QLabel("❌ Çözüm verisi alınamadı.")
            err.setStyleSheet("color: red;")
            self.review_container.addWidget(err)
            return

        data = result["review"]

        # taken_at'ı tarih formatına çevir (sadeleştirme isteğe bağlı)
        taken_at_str = data.get("taken_at", "")[:16].replace("T", " ")  # "2025-05-27 00:01"

        quiz_info = QLabel(
            f"🧪 {data['quiz_title']} | Skor: {data['score']} | Doğru: {data['correct_count']}/{data['total_questions']} | 🕒 {taken_at_str}"
        )
        quiz_info.setStyleSheet("color: white; font-size: 14px; margin-bottom: 10px;")
        self.review_container.addWidget(quiz_info)

        for q in data["questions"]:
            self.add_question_review(q)

    def add_question_review(self, q):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        layout = QVBoxLayout(frame)

        q_text = QLabel(f"❓ {q['content']}")
        q_text.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(q_text)

        q_type = q.get("question_type", "").strip().lower()

        if q_type == "open ended":
            # Kullanıcının cevabı
            user_answer = q.get("user_answer", "❌ Cevap verilmedi")
            user_ans = QLabel(f"🧍 Senin Cevabın: {user_answer}")
            user_ans.setStyleSheet("color: #555;")
            layout.addWidget(user_ans)

            # Beklenen doğru cevap
            expected_answer = q.get("expected_answer", "❓ Beklenen cevap belirtilmemiş")
            correct_ans = QLabel(f"✅ Beklenen Cevap: {expected_answer}")
            correct_ans.setStyleSheet("color: green;")
            layout.addWidget(correct_ans)

            # Doğru/Yanlış
            if q.get("is_correct", False):
                result_label = QLabel("✅ Doğru")
                result_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                result_label = QLabel("❌ Yanlış")
                result_label.setStyleSheet("color: red; font-weight: bold;")
            layout.addWidget(result_label)

        else:
            # Kullanıcının seçtiği şık
            selected = next((opt for opt in q["options"] if opt["id"] == q.get("user_selected_option_id")), None)
            selected_text = selected["option_text"] if selected else "❌ Cevap verilmedi"
            user_ans = QLabel(f"🧍 Senin Cevabın: {selected_text}")
            user_ans.setStyleSheet("color: #555;")
            layout.addWidget(user_ans)

            # Doğru şık
            correct = next((opt for opt in q["options"] if opt["is_correct"]), None)
            correct_text = correct["option_text"] if correct else "Belirtilmemiş"
            correct_ans = QLabel(f"✅ Doğru Cevap: {correct_text}")
            correct_ans.setStyleSheet("color: green;")
            layout.addWidget(correct_ans)

            # Yanlışsa uyarı etiketi
            if selected and selected["id"] != correct["id"]:
                wrong_label = QLabel("❌ Yanlış")
                wrong_label.setStyleSheet("color: red; font-weight: bold;")
                layout.addWidget(wrong_label)
            else:
                correct_label = QLabel("✅ Doğru")
                correct_label.setStyleSheet("color: green; font-weight: bold;")
                layout.addWidget(correct_label)

        # Açıklama ortak
        if q.get("explanation"):
            explanation = QLabel(f"📘 Açıklama: {q['explanation']}")
            explanation.setStyleSheet("color: #666; font-style: italic;")
            explanation.setWordWrap(True)
            layout.addWidget(explanation)

        self.review_container.addWidget(frame)
