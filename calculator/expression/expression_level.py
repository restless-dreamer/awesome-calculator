from math import *
from calculator.language_content import get_error_text


class ExpressionLevel:
    def __init__(self, language, items, pos=0):
        self.__items = []
        self.end_pos = None
        self.error = None
        self.error_pos = None
        self.error_group = None
        self.language = language
        while pos < len(items):
            if items[pos] == '(':
                next_level = ExpressionLevel(self.language, items, pos + 1)
                pos = next_level.end_pos
                result = next_level.get_result()
                if result is None:
                    self.error = next_level.error
                    self.error_pos = next_level.error_pos
                    self.error_group = next_level.error_group
                    break
                self.__items.append(result)
            elif items[pos] == ')':
                self.end_pos = pos
                break
            else:
                self.__items.append([items[pos], pos])
            pos += 1

    def calculate(self):
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == 'p':
                self.__items[pos][0] = pi
            elif self.__items[pos][0] == 'e':
                self.__items[pos][0] = e
            elif self.__items[pos][0] == 't':
                self.__items[pos][0] = tau
            pos += 1
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == '√':
                number = float(self.__items[pos + 1][0])
                if number < 0:
                    self.error = get_error_text(self.language, '√')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 3
                    return None
                result = pow(number, 0.5)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'deg':
                number = float(self.__items[pos + 1][0])
                result = degrees(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'rad':
                number = float(self.__items[pos + 1][0])
                result = radians(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'exp':
                number = float(self.__items[pos + 1][0])
                result = exp(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'abs':
                number = float(self.__items[pos + 1][0])
                result = abs(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'log':
                number = float(self.__items[pos + 1][0])
                result = log10(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'ln':
                number = float(self.__items[pos + 1][0])
                result = log(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'sin':
                number = float(self.__items[pos + 1][0])
                result = sin(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'cos':
                number = float(self.__items[pos + 1][0])
                result = cos(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'tan':
                number = float(self.__items[pos + 1][0])
                result = tan(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'sinh':
                number = float(self.__items[pos + 1][0])
                result = sinh(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'cosh':
                number = float(self.__items[pos + 1][0])
                result = cosh(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'tanh':
                number = float(self.__items[pos + 1][0])
                result = tanh(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'asin':
                number = float(self.__items[pos + 1][0])
                if number < -1 or number > 1:
                    self.error = get_error_text(self.language, 'asin')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 4
                    return None
                result = asin(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'acos':
                number = float(self.__items[pos + 1][0])
                if number < -1 or number > 1:
                    self.error = get_error_text(self.language, 'acos')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 4
                    return None
                result = acos(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'atan':
                number = float(self.__items[pos + 1][0])
                result = atan(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'asinh':
                number = float(self.__items[pos + 1][0])
                result = asinh(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'acosh':
                number = float(self.__items[pos + 1][0])
                if number < 1:
                    self.error = get_error_text(self.language, 'acosh')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 4
                    return None
                result = acosh(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            elif self.__items[pos][0] == 'atanh':
                number = float(self.__items[pos + 1][0])
                if number <= -1 or number >= 1:
                    self.error = get_error_text(self.language, 'atanh')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 4
                    return None
                result = atanh(number)
                self.__items[pos][0] = result
                self.__items.pop(pos + 1)
            pos += 1
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == '−':
                if pos == 0 or self.__items[pos - 1][0] == '(':
                    number = float(self.__items[pos + 1][0])
                    result = number * (-1)
                    self.__items[pos][0] = result
                    self.__items.pop(pos + 1)
            pos += 1
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == '!':
                number = float(self.__items[pos - 1][0])
                if 0 > number or number != int(number):
                    self.error = get_error_text(self.language, '!')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 2
                    return None
                result = factorial(number)
                self.__items[pos - 1][0] = result
                self.__items.pop(pos)
                pos -= 1
            elif self.__items[pos][0] == '%':
                number_a = float(self.__items[pos - 1][0])
                if pos == 1 or self.__items[pos - 2][0] in ['÷', '^']:
                    result = number_a / 100
                    self.__items[pos - 1][0] = result
                    self.__items.pop(pos)
                    pos -= 1
                elif pos > 1 and self.__items[pos - 2][0] in ['+', '−', '×']:
                    number_b = float(self.__items[pos - 3][0])
                    result = None
                    if self.__items[pos - 2][0] == '+':
                        result = number_b + number_b / 100 * number_a
                    elif self.__items[pos - 2][0] == '−':
                        result = number_b - number_b / 100 * number_a
                    elif self.__items[pos - 2][0] == '×':
                        result = number_b / 100 * number_a
                    self.__items[pos - 3][0] = result
                    self.__items.pop(pos)
                    self.__items.pop(pos - 1)
                    self.__items.pop(pos - 2)
                    pos -= 3
            pos += 1
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == '^':
                number_a = float(self.__items[pos - 1][0])
                number_b = float(self.__items[pos + 1][0])
                if number_a < 0 and int(number_b) != number_b \
                        or number_a == 0 and number_b < 0:
                    self.error = get_error_text(self.language, '^')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 1
                    return None
                result = pow(number_a, number_b)
                self.__items[pos - 1][0] = result
                self.__items.pop(pos)
                self.__items.pop(pos)
                pos -= 1
            pos += 1
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == '×':
                number_a = float(self.__items[pos - 1][0])
                number_b = float(self.__items[pos + 1][0])
                result = number_a * number_b
                self.__items[pos - 1][0] = result
                self.__items.pop(pos)
                self.__items.pop(pos)
                pos -= 1
            elif self.__items[pos][0] == '÷':
                number_a = float(self.__items[pos - 1][0])
                number_b = float(self.__items[pos + 1][0])
                if number_b == 0:
                    self.error = get_error_text(self.language, '÷')
                    self.error_pos = self.__items[pos][1]
                    self.error_group = 1
                    return None
                result = number_a / number_b
                self.__items[pos - 1][0] = result
                self.__items.pop(pos)
                self.__items.pop(pos)
                pos -= 1
            pos += 1
        pos = 0
        while pos < len(self.__items):
            if self.__items[pos][0] == '+':
                number_a = float(self.__items[pos - 1][0])
                number_b = float(self.__items[pos + 1][0])
                result = number_a + number_b
                self.__items[pos - 1][0] = result
                self.__items.pop(pos)
                self.__items.pop(pos)
                pos -= 1
            elif self.__items[pos][0] == '−':
                number_a = float(self.__items[pos - 1][0])
                number_b = float(self.__items[pos + 1][0])
                result = number_a - number_b
                self.__items[pos - 1][0] = result
                self.__items.pop(pos)
                self.__items.pop(pos)
                pos -= 1
            pos += 1
        return self.__items[0]

    def get_result(self):
        if self.error is not None:
            return None
        elif len(self.__items) == 1:
            number = self.__items[0][0]
            if number == 'p':
                return [pi, 0]
            elif number == 'e':
                return [e, 0]
            elif number == 't':
                return [tau, 0]
            try:
                int(float(number))
            except OverflowError:
                self.set_overflow_error()
                return None
            if len(number) > 87:
                self.set_overflow_error()
                return None
            return [float(number), 0]
        result = None
        try:
            result = self.calculate()
            if self.error is None:
                try:
                    int(result[0])
                except OverflowError:
                    self.set_overflow_error()
                    return None
        except OverflowError:
            self.set_overflow_error()
        if self.error is None:
            if int(result[0]) == result[0]:
                result_str = str(int(result[0]))
                if len(result_str) > 87:
                    self.set_overflow_error()
                    return None
            else:
                result_str = str(result[0])
                if 'e' in list(result_str):
                    from calculator.calculator_engine \
                        import convert_e_type_to_decimal
                    result_str = convert_e_type_to_decimal(result_str)
                if len(result_str) > 87:
                    self.set_overflow_error()
                    return None
        return result

    def set_overflow_error(self):
        self.error = get_error_text(self.language, 'overflow')
        self.error_pos = self.__items[0][1]
        self.error_group = 0
