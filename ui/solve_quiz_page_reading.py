import json
import pyttsx3
from threading import Thread

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QRadioButton, QButtonGroup, QTextEdit, QHBoxLayout,
    QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt

from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class SolveQuizPageReading(QWidget):
    def __init__(self, main_app, quiz_id):
        super().__init__()
        self.main_app = main_app
        self.quiz_id = quiz_id
        self.api = main_app.api

        # Set window size
        self.setMinimumSize(900, 800)  # Reduced height to encourage scrolling
        # allow free resizing by removing any maximum size constraint

        self.quiz_data = None
        self.questions = []
        self.current_index = 0
        self.answers = {}

        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)

        # Create main scroll area that wraps everything
        main_scroll = QScrollArea(self)
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Create the main container widget
        self.main_container = QWidget()
        
        # Set up the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(main_scroll)
        
        # Set the main container as the scroll area widget
        main_scroll.setWidget(self.main_container)
        
        self.setup_ui()
        self.load_quiz()

    def setup_ui(self):
        # Apply window background
        self.setStyleSheet(WINDOW_STYLE)
        self.main_container.setStyleSheet(WINDOW_STYLE)

        # Main layout with proper margins
        self.layout = QVBoxLayout(self.main_container)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setAlignment(Qt.AlignTop)

        # Header container
        header_container = QFrame()
        header_container.setFixedHeight(60)
        header_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(10, 0, 10, 0)

        # Title
        self.title = QLabel("Quiz Yükleniyor...")
        self.title.setFont(TITLE_FONT)
        self.title.setStyleSheet(TITLE_STYLE + "font-size: 20px;")
        header_layout.addWidget(self.title)

        # Back button
        back_button = QPushButton("← Geri")
        back_button.setFixedSize(100, 40)
        back_button.setFont(DEFAULT_FONT)
        back_button.setStyleSheet(BUTTON_STYLE + "font-size: 14px;")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.stop_and_back)
        header_layout.addWidget(back_button)

        self.layout.addWidget(header_container)

        # Reading passage container
        reading_container = QFrame()
        reading_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 12px;
                min-height: 250px;
            }}
            QLabel {{
                color: {COLORS['text']};
                font-size: 14px;
                line-height: 1.4;
                padding: 8px;
            }}
        """)
        reading_layout = QVBoxLayout(reading_container)
        reading_layout.setSpacing(8)
        reading_layout.setContentsMargins(8, 8, 8, 8)

        # Create a scroll area for reading text
        reading_scroll = QScrollArea()
        reading_scroll.setWidgetResizable(True)
        reading_scroll.setMinimumHeight(200)
        reading_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        reading_content = QWidget()
        reading_content_layout = QVBoxLayout(reading_content)
        reading_content_layout.setContentsMargins(5, 5, 5, 5)
        reading_content_layout.setSpacing(8)
        
        # Reading text
        self.reading_label = QLabel()
        self.reading_label.setWordWrap(True)
        self.reading_label.setFont(DEFAULT_FONT)
        self.reading_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.reading_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )
        reading_content_layout.addWidget(self.reading_label)
        reading_content_layout.addStretch()
        
        reading_scroll.setWidget(reading_content)
        reading_layout.addWidget(reading_scroll)

        # Audio control buttons
        audio_container = QFrame()
        audio_container.setFixedHeight(55)
        audio_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border-radius: 8px;
                padding: 8px;
                margin-top: 8px;
            }}
        """)
        audio_layout = QHBoxLayout(audio_container)
        audio_layout.setSpacing(10)
        audio_layout.setContentsMargins(8, 3, 8, 3)

        self.reading_button = QPushButton("🔊 Metni Oku")
        self.reading_button.setFixedSize(180, 40)
        self.reading_button.setFont(DEFAULT_FONT)
        self.reading_button.setStyleSheet(BUTTON_STYLE + "font-size: 14px;")
        self.reading_button.setCursor(Qt.PointingHandCursor)
        self.reading_button.clicked.connect(self.read_reading_text)
        audio_layout.addWidget(self.reading_button)

        self.question_button = QPushButton("🔊 Soruyu Oku")
        self.question_button.setFixedSize(180, 40)
        self.question_button.setFont(DEFAULT_FONT)
        self.question_button.setStyleSheet(BUTTON_STYLE + "font-size: 14px;")
        self.question_button.setCursor(Qt.PointingHandCursor)
        self.question_button.clicked.connect(self.read_question_aloud)
        audio_layout.addWidget(self.question_button)

        reading_layout.addWidget(audio_container)
        self.layout.addWidget(reading_container)

        # Question container
        question_container = QFrame()
        question_container.setMinimumHeight(180)
        question_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 12px;
            }}
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 14px;
                padding: 6px;
                spacing: 8px;
                min-height: 28px;
            }}
            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
            }}
            QRadioButton::indicator:unchecked {{
                background-color: {COLORS['white']};
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['primary']};
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
            }}
            QRadioButton:hover {{
                background-color: {COLORS['background']};
                border-radius: 5px;
            }}
            QTextEdit {{
                background-color: {COLORS['background']};
                border: 2px solid {COLORS['primary']};
                border-radius: 5px;
                padding: 8px;
                color: {COLORS['text']};
                font-size: 14px;
                min-height: 90px;
            }}
        """)
        question_layout = QVBoxLayout(question_container)
        question_layout.setSpacing(8)
        question_layout.setContentsMargins(8, 8, 8, 8)

        # Question text
        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        self.question_label.setFont(DEFAULT_FONT)
        self.question_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 14px; min-height: 40px; padding: 5px;")
        question_layout.addWidget(self.question_label)

        # Options scroll area
        options_scroll = QScrollArea()
        options_scroll.setWidgetResizable(True)
        options_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        options_scroll.setMinimumHeight(150)
        options_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        options_widget = QWidget()
        self.options_layout = QVBoxLayout(options_widget)
        self.options_layout.setSpacing(6)
        self.options_layout.setContentsMargins(4, 4, 4, 4)
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
        nav_container.setFixedHeight(60)
        nav_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton {{
                min-width: 120px;
                min-height: 35px;
                font-size: 14px;
            }}
        """)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 0, 10, 0)

        self.next_button = QPushButton("Sonraki →")
        self.next_button.setFont(DEFAULT_FONT)
        self.next_button.setStyleSheet(BUTTON_STYLE + "font-size: 14px;")
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.clicked.connect(self.stop_and_next)
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
                min-width: 120px;
                min-height: 40px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #7FD17F;
                color: {COLORS['white']};
            }}
        """)
        self.finish_button.setCursor(Qt.PointingHandCursor)
        self.finish_button.clicked.connect(self.stop_and_finish)
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
            self.question_label.setText("🎉 Quiz tamamlandı!")
            self.next_button.hide()
            self.finish_button.hide()
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
        self._set_buttons_enabled(False)

        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

        self._set_buttons_enabled(True)

    def _set_buttons_enabled(self, enabled: bool):
        # Update button states and styles
        if not enabled:
            self.reading_button.setText("🔊 Metin okunuyor...")
            self.reading_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['background']};
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    color: {COLORS['text']};
                }}
            """)
            
            self.question_button.setText("🔊 Soru okunuyor...")
            self.question_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['background']};
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    color: {COLORS['text']};
                }}
            """)
            
            self.next_button.setText("⏳")
            self.finish_button.setText("⏳")
        else:
            self.reading_button.setText("🔊 Metni Oku")
            self.reading_button.setStyleSheet(BUTTON_STYLE)
            
            self.question_button.setText("🔊 Soruyu Oku")
            self.question_button.setStyleSheet(BUTTON_STYLE)
            
            self.next_button.setText("Sonraki →")
            self.finish_button.setText("✓ Bitir ve Gönder")

        # Enable/disable buttons
        self.reading_button.setEnabled(enabled)
        self.question_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)
        self.finish_button.setEnabled(enabled)

