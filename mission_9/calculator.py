import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt



class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')
        self.setFixedSize(400, 500)
        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('C', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        for button in buttons:
            if len(button) == 3:
                text, row, col = button
                colspan = 1
            else:
                text, row, col, rowspan, colspan = button
            btn = QPushButton(text)
            btn.setFixedHeight(60)
            btn.clicked.connect(self.on_button_clicked)
            self.layout.addWidget(btn, row, col, 1, colspan)

    def on_button_clicked(self):
        button = self.sender()
        text = button.text()
        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                expression = self.display.text()
                result = str(eval(expression))
                self.display.setText(result)
            except Exception:
                self.display.setText('계산 오류')
        else:
            self.display.setText(self.display.text() + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
