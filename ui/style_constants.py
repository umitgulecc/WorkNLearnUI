from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt

# Color Palette
COLORS = {
    'primary': '#A7C7E7',      # Light pastel blue
    'secondary': '#C6E2FF',    # Lighter pastel blue
    'accent': '#6495ED',       # Cornflower blue
    'background': '#F0F8FF',   # Alice blue
    'text': '#2C3E50',         # Dark blue-grey
    'white': '#FFFFFF',        # Pure white
    'error': '#FFB6C1',        # Light pink for errors
    'success': '#90EE90',      # Light green for success
}

# Styles
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['primary']};
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        color: {COLORS['text']};
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['accent']};
        color: {COLORS['white']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['secondary']};
    }}
"""

INPUT_STYLE = f"""
    QLineEdit, QTextEdit, QComboBox {{
        background-color: {COLORS['white']};
        border: 2px solid {COLORS['primary']};
        border-radius: 5px;
        padding: 8px;
        color: {COLORS['text']};
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 2px solid {COLORS['accent']};
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text']};
        font-size: 14px;
    }}
"""

TITLE_STYLE = f"""
    QLabel {{
        color: {COLORS['text']};
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
    }}
"""

LIST_STYLE = f"""
    QListWidget {{
        background-color: {COLORS['white']};
        border: 2px solid {COLORS['primary']};
        border-radius: 5px;
        padding: 5px;
    }}
    QListWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {COLORS['secondary']};
    }}
    QListWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['text']};
    }}
"""

WINDOW_STYLE = f"""
    QWidget {{
        background-color: {COLORS['background']};
    }}
"""

# Common Fonts
DEFAULT_FONT = QFont('Segoe UI', 10)
TITLE_FONT = QFont('Segoe UI', 16, QFont.Bold)
BUTTON_FONT = QFont('Segoe UI', 10, QFont.Medium)

# Layout Constants
SPACING = 20
MARGINS = (20, 20, 20, 20)  # left, top, right, bottom 