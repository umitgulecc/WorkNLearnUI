import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QButtonGroup, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt
from utils.style import APP_STYLE

class SolveQuizPage(QWidget):
    def __init__(self, main_app, quiz_id):
        super().__init__()
        self.main_app = main_app
        self.quiz_id = quiz_id
        self.api = main_app.api

        self.quiz_data = None
        self.questions = []
        self.current_index = 0
        self.answers = {}

        self.setup_ui()
        self.load_quiz()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Quiz Yükleniyor...")
        self.title.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(self.title)

        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 16px; color: white;")
        self.layout.addWidget(self.question_label)

        self.option_group = QButtonGroup(self)
        self.options_layout = QVBoxLayout()
        self.layout.addLayout(self.options_layout)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Cevabınızı buraya yazınız...")
        self.layout.addWidget(self.text_input)
        self.text_input.hide()

        button_row = QHBoxLayout()

        self.next_button = QPushButton("Sonraki")
        self.next_button.clicked.connect(self.save_and_next)
        button_row.addWidget(self.next_button)

        self.finish_button = QPushButton("Bitir ve Gönder")
        self.finish_button.clicked.connect(self.finish_quiz)
        button_row.addWidget(self.finish_button)
        self.finish_button.hide()

        self.layout.addLayout(button_row)


        back_button = QPushButton("← Geri")
        back_button.clicked.connect(lambda: self.main_app.go_to_quiz())
        self.layout.addWidget(back_button)

    def load_quiz(self):
        result = self.api.get_quiz(self.quiz_id)
        if result["success"]:
            self.quiz_data = result["quiz"]
            self.questions = self.quiz_data["questions"]
            self.title.setText(f"📘 {self.quiz_data['title']}")
            self.display_question()
        else:
            self.title.setText("❌ Quiz yüklenemedi.")
            self.question_label.setText(result["detail"])

    def display_question(self):
        self.clear_question_ui()

        if self.current_index >= len(self.questions):
            self.question_label.setText("🎉 Quiz tamamlandı.")
            self.next_button.hide()
            self.finish_button.hide()
            return

        question = self.questions[self.current_index]
        question_text = question.get("content", "Soru yok")
        self.question_label.setText(f"{self.current_index+1}. Soru: {question_text}")

        q_type = question.get("question_type", "").lower()
        if "multiple" in q_type:
            self.text_input.hide()
            self.option_group = QButtonGroup(self)
            for option in question.get("options", []):
                btn = QRadioButton(option["option_text"])
                btn.setProperty("option_id", option["id"])
                self.options_layout.addWidget(btn)
                self.option_group.addButton(btn)
        else:
            self.text_input.show()

        # Butonları ayarla
        if self.current_index == len(self.questions) - 1:
            self.next_button.hide()
            self.finish_button.show()
        else:
            self.next_button.show()
            self.finish_button.hide()


    def clear_question_ui(self):
        # Seçenekleri temizle
        for i in reversed(range(self.options_layout.count())):
            widget = self.options_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.option_group = QButtonGroup(self)

        self.text_input.clear()
        self.text_input.hide()

    def save_answer(self):
        question = self.questions[self.current_index]
        qid = question["id"]
        q_type = question.get("question_type", "").lower().strip()

        if q_type == "multiple choise":
            checked = self.option_group.checkedButton()
            if checked:
                self.answers[qid] = {
                    "selected_option_id": checked.property("option_id"),
                    "written_answer": ""
                }

        elif q_type == "open ended":
            self.answers[qid] = {
                "selected_option_id": None,
                "written_answer": self.text_input.toPlainText().strip()
            }

    def save_and_next(self):
        if self.current_index < len(self.questions):
            self.save_answer()
            self.current_index += 1
            self.display_question()

    def finish_quiz(self):
        self.save_answer()

        payload = {
            "quiz_id": self.quiz_id,
            "answers": []
        }

        for qid, answer in self.answers.items():
            payload["answers"].append({
                "question_id": qid,
                "selected_option_id": answer.get("selected_option_id"),
                "written_answer": answer.get("written_answer", "")
            })

        print("📤 Gönderilen Payload:\n", json.dumps(payload, indent=2))  # Debug için

        result = self.api.submit_quiz(payload)
        if result["success"]:
            print("✅ Quiz gönderildi:", result)
            self.title.setText(f"✅ Quiz gönderildi, skor: {result['score']}")
        else:
            self.title.setText("❌ Gönderme başarısız: " + result["detail"])

