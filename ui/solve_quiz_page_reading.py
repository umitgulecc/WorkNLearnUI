import json
import pyttsx3
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QButtonGroup, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt
from utils.style import APP_STYLE
from threading import Thread

class SolveQuizPageReading(QWidget):
    def __init__(self, main_app, quiz_id):
        super().__init__()
        self.main_app = main_app
        self.quiz_id = quiz_id
        self.api = main_app.api

        self.quiz_data = None
        self.questions = []
        self.current_index = 0
        self.answers = {}

        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)

        self.setup_ui()
        self.load_quiz()

    def setup_ui(self):
        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Quiz Yükleniyor...")
        self.title.setStyleSheet("font-size: 18px; color: white;")
        self.layout.addWidget(self.title)

        self.reading_label = QLabel()
        self.reading_label.setWordWrap(True)
        self.reading_label.setStyleSheet("font-size: 14px; color: white; background-color: #333; padding: 8px; border-radius: 5px;")
        self.layout.addWidget(self.reading_label)
        self.reading_label.hide()
        
        # 🔊 2 ayrı buton satırı
        self.audio_button_row = QHBoxLayout()

        self.reading_button = QPushButton("🔊 Metni Oku")
        self.reading_button.clicked.connect(self.read_reading_text)
        self.reading_button.hide()
        self.audio_button_row.addWidget(self.reading_button)

        self.question_button = QPushButton("🔊 Soruyu Oku")
        self.question_button.clicked.connect(self.read_question_aloud)
        self.question_button.hide()
        self.audio_button_row.addWidget(self.question_button)

        self.layout.addLayout(self.audio_button_row)

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

        self.next_button = QPushButton("Sonraki \n(Soruya geri dönemeyecğini unutma!)")
        self.next_button.clicked.connect(self.stop_and_next)
        button_row.addWidget(self.next_button)

        self.finish_button = QPushButton("Bitir ve Gönder")
        self.finish_button.clicked.connect(self.stop_and_finish)
        button_row.addWidget(self.finish_button)
        self.finish_button.hide()

        self.layout.addLayout(button_row)

        back_button = QPushButton("← Quizden Çık")
        back_button.clicked.connect(self.stop_and_back)
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
        self.question_label.setText(f"{self.current_index + 1}. Soru: {question_text}")

        if self.current_index == 0:
            passage_title = question.get("reading_passage_title")
            passage_content = question.get("reading_passage_content")

            if passage_title or passage_content:
                reading_text = ""
                if passage_title:
                    reading_text += f"📘 {passage_title}\n\n"
                if passage_content:
                    reading_text += passage_content

                self.reading_label.setText(reading_text)
                self.reading_label.show()
                self.reading_button.show()
                self.question_button.show()
            else:
                self.reading_label.hide()
                self.reading_button.hide()
                self.question_button.hide()
        else:
            self.reading_label.hide()
            self.reading_button.hide()
            self.question_button.show()

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

        if self.current_index == len(self.questions) - 1:
            self.next_button.hide()
            self.finish_button.show()
        else:
            self.next_button.show()
            self.finish_button.hide()

    def clear_question_ui(self):
        for i in reversed(range(self.options_layout.count())):
            widget = self.options_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.option_group = QButtonGroup(self)

        self.text_input.clear()
        self.text_input.hide()

    def read_question_aloud(self):
        if self.current_index < len(self.questions):
            question = self.questions[self.current_index]
            question_text = question.get("content", "")
            if question_text.strip():
                Thread(target=self._speak, args=(question_text,), daemon=True).start()


    def read_reading_text(self):
        reading_text = self.reading_label.text()
        if reading_text.strip():
            Thread(target=self._speak, args=(reading_text,), daemon=True).start()

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

        print("📤 Gönderilen Payload:\n", json.dumps(payload, indent=2))

        result = self.api.submit_quiz(payload)
        if result["success"]:
            print("✅ Quiz gönderildi:", result)
            self.title.setText(f"✅ Quiz gönderildi, skor: {result['score']}")
        else:
            self.title.setText("❌ Gönderme başarısız: " + result["detail"])


    def stop_and_next(self):
        self.tts_engine.stop()
        self.save_and_next()

    def stop_and_finish(self):
        self.tts_engine.stop()
        self.finish_quiz()

    def stop_and_back(self):
        self.tts_engine.stop()
        self.main_app.go_to_quiz()

    def _speak(self, text):
        self._set_buttons_enabled(False)  # 👇 butonları kilitle

        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

        self._set_buttons_enabled(True)  # ✅ okuma bitince aç


    def _set_buttons_enabled(self, enabled: bool):
        # Okuma sırasında görsel olarak değiştir
        if not enabled:
            self.reading_button.setText("🔒 Metin okunuyor...")
            self.question_button.setText("🔒 Soru okunuyor...")
            self.next_button.setText("⏳")
            self.finish_button.setText("⏳")
        else:
            self.reading_button.setText("🔊 Metni Oku")
            self.question_button.setText("🔊 Soruyu Oku")
            self.next_button.setText("Sonraki \n(Soruya geri dönemeyeceğini unutma!)")
            self.finish_button.setText("Bitir ve Gönder")

        # Butonları etkin/pasif yap
        self.reading_button.setEnabled(enabled)
        self.question_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)
        self.finish_button.setEnabled(enabled)

