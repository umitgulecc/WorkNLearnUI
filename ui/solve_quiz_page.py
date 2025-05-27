import json
import pyttsx3
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QButtonGroup, QTextEdit, QHBoxLayout,
    QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

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

        # 🎙 TTS motoru
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)

        self.setup_ui()
        self.load_quiz()

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
        self.title = QLabel("Quiz Yükleniyor...")
        self.title.setFont(TITLE_FONT)
        self.title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(self.title)

        # Back button
        back_button = QPushButton("← Geri")
        back_button.setFont(DEFAULT_FONT)
        back_button.setStyleSheet(BUTTON_STYLE)
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(lambda: self.main_app.go_to_quiz())
        header_layout.addWidget(back_button)

        self.layout.addWidget(header_container)

        # Question container
        question_container = QFrame()
        question_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 14px;
                padding: 8px;
                spacing: 10px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:unchecked {{
                background-color: {COLORS['white']};
                border: 2px solid {COLORS['primary']};
                border-radius: 10px;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['primary']};
                border: 2px solid {COLORS['primary']};
                border-radius: 10px;
            }}
            QRadioButton:hover {{
                background-color: {COLORS['background']};
                border-radius: 5px;
            }}
            QTextEdit {{
                background-color: {COLORS['background']};
                border: 2px solid {COLORS['primary']};
                border-radius: 5px;
                padding: 10px;
                color: {COLORS['text']};
                font-size: 14px;
            }}
            QTextEdit:focus {{
                border: 2px solid {COLORS['accent']};
            }}
        """)
        question_layout = QVBoxLayout(question_container)
        question_layout.setSpacing(SPACING)

        # Question text
        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        self.question_label.setFont(DEFAULT_FONT)
        self.question_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 16px;")
        question_layout.addWidget(self.question_label)

        # Options
        options_scroll = QScrollArea()
        options_scroll.setWidgetResizable(True)
        options_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        options_widget = QWidget()
        self.options_layout = QVBoxLayout(options_widget)
        self.options_layout.setSpacing(SPACING // 2)
        self.option_group = QButtonGroup(self)
        
        options_scroll.setWidget(options_widget)
        question_layout.addWidget(options_scroll)

        # Text input for open-ended questions
        self.text_input = QTextEdit()
        self.text_input.setFont(DEFAULT_FONT)
        self.text_input.setPlaceholderText("Cevabınızı buraya yazınız...")
        self.text_input.setMinimumHeight(100)
        question_layout.addWidget(self.text_input)
        self.text_input.hide()

        self.layout.addWidget(question_container)

        # Navigation buttons container
        nav_container = QFrame()
        nav_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setSpacing(SPACING)

        self.next_button = QPushButton("Sonraki →")
        self.next_button.setFont(DEFAULT_FONT)
        self.next_button.setStyleSheet(BUTTON_STYLE)
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.clicked.connect(self.save_and_next)
        nav_layout.addWidget(self.next_button)

        self.finish_button = QPushButton("✓ Bitir ve Gönder")
        self.finish_button.setFont(DEFAULT_FONT)
        self.finish_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                color: {COLORS['text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #7FD17F;
                color: {COLORS['white']};
            }}
        """)
        self.finish_button.setCursor(Qt.PointingHandCursor)
        self.finish_button.clicked.connect(self.finish_quiz)
        nav_layout.addWidget(self.finish_button)
        self.finish_button.hide()

        self.layout.addWidget(nav_container)

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
                btn.setFont(DEFAULT_FONT)
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
            self.tts_engine.say(question_text)
            self.tts_engine.runAndWait()

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
