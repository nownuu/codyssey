import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class CalculatorLogic:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_value = '0'
        self.operator = ''
        self.operand = None
        self.pending_operator = False

    def add(self):
        self._calculate_pending()
        self.operator = '+'
        self.operand = float(self.current_value)
        self.pending_operator = True

    def subtract(self):
        self._calculate_pending()
        self.operator = '-'
        self.operand = float(self.current_value)
        self.pending_operator = True

    def multiply(self):
        self._calculate_pending()
        self.operator = '*'
        self.operand = float(self.current_value)
        self.pending_operator = True

    def divide(self):
        self._calculate_pending()
        self.operator = '/'
        self.operand = float(self.current_value)
        self.pending_operator = True

    def negative_positive(self):
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            if self.current_value != '0':
                self.current_value = '-' + self.current_value

    def percent(self):
        try:
            value = float(self.current_value)
            self.current_value = str(value / 100)
        except ValueError:
            self.current_value = '계산 오류'

    def equal(self):
        self._calculate_pending()
        self.operator = ''
        self.operand = None

    def _calculate_pending(self):
        try:
            if self.operator and self.operand is not None:
                right = float(self.current_value)
                if self.operator == '+':
                    result = self.operand + right
                elif self.operator == '-':
                    result = self.operand - right
                elif self.operator == '*':
                    result = self.operand * right
                elif self.operator == '/':
                    if right == 0:
                        self.current_value = '0으로 나눌 수 없음'
                        return
                    result = self.operand / right

                # 정수면 int로 변환
                if isinstance(result, float) and result.is_integer():
                    result = int(result)

                self.current_value = str(result)
                self.operand = None
        except Exception:
            self.current_value = '계산 오류'


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')
        self.setFixedSize(400, 500)
        self.calculator = CalculatorLogic()
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

        self.update_display()

    def on_button_clicked(self):
        button = self.sender()
        text = button.text()
        curr = self.calculator.current_value

        if text == 'C':
            self.calculator.reset()
        elif text == '+/-':
            self.calculator.negative_positive()
        elif text == '%':
            self.calculator.percent()
        elif text == '=':
            self.calculator.equal()
        elif text == '+':
            self.calculator.add()
        elif text == '-':
            self.calculator.subtract()
        elif text == '*':
            self.calculator.multiply()
        elif text == '/':
            self.calculator.divide()
        elif text == '.':
            if self.calculator.pending_operator:
                self.calculator.current_value = '0.'
                self.calculator.pending_operator = False
            elif '.' not in curr:
                self.calculator.current_value += '.'
        elif text.isdigit():
            if curr == '0' or self.calculator.pending_operator:
                self.calculator.current_value = text
                self.calculator.pending_operator = False
            else:
                self.calculator.current_value += text

        self.update_display()

    def update_display(self):
        self.display.setText(self.calculator.current_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
