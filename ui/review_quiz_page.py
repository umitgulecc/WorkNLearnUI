from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from .style_constants import (
    COLORS, BUTTON_STYLE, WINDOW_STYLE, TITLE_STYLE,
    TITLE_FONT, DEFAULT_FONT, SPACING, MARGINS
)

class ReviewQuizPage(QWidget):
    def __init__(self, main_app, result_id, user_id=None): 
        super().__init__()
        self.main_app = main_app
        self.api = main_app.api
        self.result_id = result_id
        self.user_id = user_id or main_app.current_user["id"]

        self.setup_ui()
        self.load_review()

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
        title = QLabel("📋 Quiz Çözüm İncelemesi")
        title.setFont(TITLE_FONT)
        title.setStyleSheet(TITLE_STYLE)
        header_layout.addWidget(title)

        # Back button
        back_button = QPushButton("← Geri")
        back_button.setFont(DEFAULT_FONT)
        back_button.setStyleSheet(BUTTON_STYLE)
        back_button.setCursor(Qt.PointingHandCursor)
        if self.user_id == self.main_app.current_user["id"]:
            back_button.clicked.connect(lambda: self.main_app.show_role_dashboard(self.main_app.current_user))
        else:
            back_button.clicked.connect(lambda: self.main_app.go_to_team_member_details(self.user_id))
        header_layout.addWidget(back_button)

        self.layout.addWidget(header_container)

        # Review container
        review_frame = QFrame()
        review_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 10px;
                padding: 20px;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {COLORS['background']};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['primary']};
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        review_layout = QVBoxLayout(review_frame)
        review_layout.setSpacing(SPACING)

        self.review_container = QVBoxLayout()
        self.review_container.setSpacing(SPACING)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.review_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        review_layout.addWidget(scroll_area)

        self.layout.addWidget(review_frame)

    def load_review(self):
        result = self.api.get_quiz_review(self.result_id)
        if not result["success"]:
            err = QLabel("❌ Çözüm verisi alınamadı.")
            err.setFont(DEFAULT_FONT)
            err.setStyleSheet(f"color: {COLORS['error']};")
            self.review_container.addWidget(err)
            return

        data = result["review"]

        # Format taken_at date
        taken_at_str = data.get("taken_at", "")[:16].replace("T", " ")

        # Quiz info container
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)

        quiz_info = QLabel(
            f"🧪 {data['quiz_title']}"
        )
        quiz_info.setFont(DEFAULT_FONT)
        quiz_info.setStyleSheet(f"color: {COLORS['text']}; font-weight: bold;")
        info_layout.addWidget(quiz_info)

        stats_info = QLabel(
            f"📊 Skor: {data['score']} | ✅ Doğru: {data['correct_count']}/{data['total_questions']} | 🕒 {taken_at_str}"
        )
        stats_info.setFont(DEFAULT_FONT)
        stats_info.setStyleSheet(f"color: {COLORS['text']};")
        info_layout.addWidget(stats_info)

        self.review_container.addWidget(info_frame)

        # Add questions
        for q in data["questions"]:
            self.add_question_review(q)

    def add_question_review(self, q):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border-radius: 8px;
                padding: 15px;
            }}
            QLabel {{
                color: {COLORS['text']};
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setSpacing(SPACING)

        # Question text
        q_text = QLabel(f"❓ {q['content']}")
        q_text.setFont(DEFAULT_FONT)
        q_text.setStyleSheet(f"color: {COLORS['text']}; font-weight: bold; font-size: 14px;")
        q_text.setWordWrap(True)
        layout.addWidget(q_text)

        q_type = q.get("question_type", "").strip().lower()

        if q_type == "open ended":
            # User's answer
            user_answer = q.get("user_answer", "❌ Cevap verilmedi")
            user_ans = QLabel(f"🧍 Senin Cevabın: {user_answer}")
            user_ans.setFont(DEFAULT_FONT)
            user_ans.setWordWrap(True)
            layout.addWidget(user_ans)

            # Expected answer
            expected_answer = q.get("expected_answer", "❓ Beklenen cevap belirtilmemiş")
            correct_ans = QLabel(f"✅ Beklenen Cevap: {expected_answer}")
            correct_ans.setFont(DEFAULT_FONT)
            correct_ans.setStyleSheet(f"color: {COLORS['success']};")
            correct_ans.setWordWrap(True)
            layout.addWidget(correct_ans)

            # Result
            if q.get("is_correct", False):
                result_label = QLabel("✅ Doğru")
                result_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            else:
                result_label = QLabel("❌ Yanlış")
                result_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")
            result_label.setFont(DEFAULT_FONT)
            layout.addWidget(result_label)

        else:
            # User's selected option
            selected = next((opt for opt in q["options"] if opt["id"] == q.get("user_selected_option_id")), None)
            selected_text = selected["option_text"] if selected else "❌ Cevap verilmedi"
            user_ans = QLabel(f"🧍 Senin Cevabın: {selected_text}")
            user_ans.setFont(DEFAULT_FONT)
            user_ans.setWordWrap(True)
            layout.addWidget(user_ans)

            # Correct option
            correct = next((opt for opt in q["options"] if opt["is_correct"]), None)
            correct_text = correct["option_text"] if correct else "Belirtilmemiş"
            correct_ans = QLabel(f"✅ Doğru Cevap: {correct_text}")
            correct_ans.setFont(DEFAULT_FONT)
            correct_ans.setStyleSheet(f"color: {COLORS['success']};")
            correct_ans.setWordWrap(True)
            layout.addWidget(correct_ans)

            # Result
            if selected and selected["id"] != correct["id"]:
                wrong_label = QLabel("❌ Yanlış")
                wrong_label.setStyleSheet(f"color: {COLORS['error']}; font-weight: bold;")
            else:
                wrong_label = QLabel("✅ Doğru")
                wrong_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            wrong_label.setFont(DEFAULT_FONT)
            layout.addWidget(wrong_label)

        # Explanation
        if q.get("explanation"):
            explanation = QLabel(f"📘 Açıklama: {q['explanation']}")
            explanation.setFont(DEFAULT_FONT)
            explanation.setStyleSheet(f"color: {COLORS['text']}; font-style: italic;")
            explanation.setWordWrap(True)
            layout.addWidget(explanation)

        self.review_container.addWidget(frame)
