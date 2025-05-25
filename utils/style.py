# utils/style.py

APP_STYLE = """
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #6fb1fc, stop:1 #4364f7);
}
QLabel {
    font-family: 'Poppins';
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
}
QLineEdit, QComboBox {
    font-family: 'Poppins';
    font-size: 14px;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background-color: #fdfdfd;
    color: #333333;
}
QPushButton {
    font-family: 'Poppins';
    font-size: 14px;
    background-color: #ffffff;
    color: #333333;
    border-radius: 8px;
    padding: 10px;
}
QPushButton:hover {
    background-color: #e6e6e6;
}
"""
