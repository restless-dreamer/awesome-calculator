from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from calculator.screens.calculator_screen import CalculatorScreen
from calculator.keyboard_queue import KeyboardQueue
from calculator.expression.parse_expression import parse_expression
from calculator.expression.expression_level import ExpressionLevel
from calculator.screens.theme_screen import ThemeScreen
from calculator.screens.language_screen import LanguageScreen
from calculator.language_content import get_error_text
from calculator.calculator_settings import CalculatorSettings


class CalculatorEngine(App):
    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)
        self.title = 'Awesome Calculator'
        self.calculator_screen = None
        self.screen_manager = None
        self.keyboard_listener = None
        self.keyboard_queue = None
        self.language = None
        self.success = None
        self.settings = None
        self.open_bracket_expressions_count = 0
        self.texts_displayed_in_expression = []
        self.groups_of_pressed_buttons = []
        self.current_result = None
        self.current_error = None
        self.current_error_cause = None
        self.running_on_desktop = None

    def build(self):
        from kivy.config import Config
        self.running_on_desktop = bool(Config.getint('kivy', 'desktop'))

        if self.running_on_desktop:
            self.icon = 'logos/desktop/logo.png'
        else:
            self.icon = 'logos/mobile/logo.png'

        self.calculator_screen = CalculatorScreen()
        self.calculator_screen.running_on_desktop = self.running_on_desktop
        self.calculator_screen.basic_calculator_buttons_disablement()

        self.settings = CalculatorSettings(self)
        scroll_y = self.settings.language_scroll_y
        language_screen = LanguageScreen(self, scroll_y)
        scroll_y = self.settings.theme_scroll_y
        theme_screen = ThemeScreen(self.settings, scroll_y)
        self.settings.add_screen(language_screen)
        self.settings.add_screen(theme_screen)
        language = self.settings.language
        language_screen.set_language(language, True)
        theme_screen.add_screen(self.calculator_screen)
        theme_screen.add_screen(language_screen)
        color = self.settings.color
        orientation = self.settings.orientation
        theme_screen.set_theme(color, orientation)
        self.settings.save()

        if self.running_on_desktop:
            from pynput.keyboard import Listener
            self.keyboard_listener = Listener(self.keyboard_button_press)
            self.keyboard_listener.start()
            self.keyboard_queue = KeyboardQueue(self)
            self.keyboard_queue.start()

        if not self.running_on_desktop:
            if Window.width > Window.height:
                self.calculator_screen.show_extended_calculator_buttons()
            else:
                self.calculator_screen.hide_extended_calculator_buttons()

        transition = FadeTransition(duration=0.1)
        self.screen_manager = ScreenManager(transition=transition)
        self.screen_manager.add_widget(self.calculator_screen)
        self.screen_manager.add_widget(theme_screen)
        self.screen_manager.add_widget(language_screen)

        return self.screen_manager

    def do_operations_for_erase_button_press(self):
        self.calculator_screen.clear_display()
        self.calculator_screen.stop_expression_highlighting()
        self.erase_last_text_and_ensure_correctness()
        if self.running_on_desktop:
            self.keyboard_queue.clear_keyboard_queue()
        self.current_result = None
        self.current_error = None

    def do_operations_for_clear_button_press(self):
        self.calculator_screen.clear_display()
        self.calculator_screen.stop_expression_highlighting()
        self.clear_expression_text_and_reset_input()
        if self.running_on_desktop:
            self.keyboard_queue.clear_keyboard_queue()
        self.current_result = None
        self.current_error = None

    def do_operations_for_equals_button_press(self):
        if self.running_on_desktop:
            self.keyboard_queue.clear_keyboard_queue()
        self.get_result_of_math_expression()

    def define_group_of_pressed_calculator_button(self, group):
        if group == 1:
            self.calculator_screen.calculator_button_of_group_1_pressed()
        elif group == 2:
            self.calculator_screen.calculator_button_of_group_2_pressed()
        elif group == 3:
            self.calculator_screen.calculator_button_of_group_3_pressed()
        elif group == 4:
            self.calculator_screen.calculator_button_of_group_4_pressed()
        elif group == 5:
            self.calculator_screen.calculator_button_of_group_5_pressed()
        elif group == 6:
            self.calculator_screen.calculator_button_of_group_6_pressed()
        elif group == 7:
            self.calculator_screen.calculator_button_of_group_7_pressed()
        elif group == 8:
            self.calculator_screen.calculator_button_of_group_8_pressed()
        elif group == 9:
            self.calculator_screen.calculator_button_of_group_9_pressed()

    def erase_last_text_and_ensure_correctness(self):
        text_rd = self.texts_displayed_in_expression[-1]
        self.calculator_screen.remove_from_displaying_text(text_rd)
        last_id = len(self.texts_displayed_in_expression) - 1
        self.texts_displayed_in_expression.pop(last_id)
        self.groups_of_pressed_buttons.pop(last_id)

        if len(self.texts_displayed_in_expression) == 0:
            self.clear_expression_text_and_reset_input()
            return

        ct_group = self.groups_of_pressed_buttons[-1]
        self.define_group_of_pressed_calculator_button(ct_group)

        self.ensure_the_correctness_of_further_input(text_rd, True)

    def clear_expression_text_and_reset_input(self):
        self.calculator_screen.clear_displaying_text()
        self.calculator_screen.basic_calculator_buttons_disablement()

        self.open_bracket_expressions_count = 0
        self.texts_displayed_in_expression.clear()
        self.groups_of_pressed_buttons.clear()

    def check_if_floating_number_is_less_than_1(self):
        if len(self.texts_displayed_in_expression) == 1:
            return True
        elif self.texts_displayed_in_expression[-2] == '(':
            return True
        elif self.groups_of_pressed_buttons[-2] == 3:
            return True
        elif self.texts_displayed_in_expression[-2] == '√':
            return True
        return False

    def ensure_the_correctness_of_further_input(self, text, back):
        if text == '(':
            if not back:
                self.open_bracket_expressions_count += 1
            elif back:
                self.open_bracket_expressions_count -= 1
                if self.open_bracket_expressions_count == 0:
                    self.calculator_screen.disable_bracket_2_button()

        elif text == ')':
            if not back:
                self.open_bracket_expressions_count -= 1
                if self.open_bracket_expressions_count == 0:
                    self.calculator_screen.disable_bracket_2_button()
                elif self.open_bracket_expressions_count > 0:
                    self.calculator_screen.disable_equals_button()
            elif back:
                self.open_bracket_expressions_count += 1
                self.calculator_screen.disable_equals_button()

        elif self.open_bracket_expressions_count == 0:
            self.calculator_screen.disable_bracket_2_button()

        elif self.open_bracket_expressions_count > 0:
            self.calculator_screen.disable_equals_button()

        if text == '0' and not back:
            if self.check_if_floating_number_is_less_than_1():
                self.calculator_screen.disable_number_buttons()

        elif self.texts_displayed_in_expression[-1] == '0' and back:
            if self.check_if_floating_number_is_less_than_1():
                self.calculator_screen.disable_number_buttons()

        if self.groups_of_pressed_buttons[-1] == 1:
            if len(self.groups_of_pressed_buttons) > 1:
                pos = len(self.groups_of_pressed_buttons) - 2
                while pos > 0:
                    if self.groups_of_pressed_buttons[pos] == 3:
                        break
                    pos -= 1
                while pos < len(self.texts_displayed_in_expression):
                    if self.texts_displayed_in_expression[pos] == ',':
                        self.calculator_screen.disable_comma_button()
                        break
                    pos += 1

    def extend_expression_with_button_text(self, text, group):
        if self.current_result is not None or \
                self.current_error is not None:
            self.calculator_screen.clear_display()
            self.calculator_screen.stop_expression_highlighting()

        self.texts_displayed_in_expression.append(text)
        self.groups_of_pressed_buttons.append(group)

        self.define_group_of_pressed_calculator_button(group)

        self.calculator_screen.add_to_displaying_text(text)

        self.ensure_the_correctness_of_further_input(text, False)

    def calculator_button_press(self, text, group):
        if text == 'E':
            self.do_operations_for_erase_button_press()
            return
        elif text == 'C':
            self.do_operations_for_clear_button_press()
            return
        elif text == '=':
            self.do_operations_for_equals_button_press()
            return

        self.extend_expression_with_button_text(text, group)

    def keyboard_button_press(self, key):
        if Window.focus:
            if self.screen_manager.current == 'calculator_screen':
                self.keyboard_queue.add_pressed_key(key)

    def analyze_pressed_key(self, key):
        from pynput.keyboard import Key
        self.calculator_screen.set_background_normal_by_default()
        if key == Key.backspace:
            if self.calculator_screen.get_button_availability('E'):
                self.do_operations_for_erase_button_press()
                self.calculator_screen.set_background_down_value('E')
                return
        elif key == Key.delete:
            if self.calculator_screen.get_button_availability('C'):
                self.do_operations_for_clear_button_press()
                self.calculator_screen.set_background_down_value('C')
                return
        elif key == Key.enter:
            if self.calculator_screen.get_button_availability('='):
                self.do_operations_for_equals_button_press()
                self.calculator_screen.set_background_down_value('=')
                return
        elif str(key) == '<65437>':
            if self.calculator_screen.get_button_availability('5'):
                self.extend_expression_with_button_text('5', 1)
                self.calculator_screen.set_background_down_value('5')
                return
        elif list(str(key))[0] == '<' and list(str(key))[-1] == '>':
            key_code_items = list(str(key))[1:-1]
            key_code_str = ''
            for key_code_item in key_code_items:
                key_code_str += key_code_item
            value = int(key_code_str) - 96
            if 0 <= value <= 9:
                text = str(value)
                if self.calculator_screen.get_button_availability(text):
                    self.extend_expression_with_button_text(text, 1)
                    self.calculator_screen.set_background_down_value(text)
            elif value == 14:
                if self.calculator_screen.get_button_availability(','):
                    self.extend_expression_with_button_text(',', 4)
                    self.calculator_screen.set_background_down_value(',')
        text = None
        try:
            text = key.char
        except AttributeError:
            pass
        if text is None:
            return
        if text in '0123456789':
            if self.calculator_screen.get_button_availability(text):
                self.extend_expression_with_button_text(text, 1)
                self.calculator_screen.set_background_down_value(text)
        elif text == ',' or text == '.':
            if self.calculator_screen.get_button_availability(','):
                self.extend_expression_with_button_text(',', 4)
                self.calculator_screen.set_background_down_value(',')
        elif text == '=':
            if self.calculator_screen.get_button_availability(text):
                self.do_operations_for_equals_button_press()
                self.calculator_screen.set_background_down_value('=')
        elif text == '+' or text == '^':
            if self.calculator_screen.get_button_availability(text):
                self.extend_expression_with_button_text(text, 3)
                self.calculator_screen.set_background_down_value('+')
        elif text == '-' or text == '−':
            if self.calculator_screen.get_button_availability('−'):
                self.extend_expression_with_button_text('−', 3)
                self.calculator_screen.set_background_down_value('−')
        elif text == '*' or text == '×':
            if self.calculator_screen.get_button_availability('×'):
                self.extend_expression_with_button_text('×', 3)
                self.calculator_screen.set_background_down_value('×')
        elif text == '/' or text == '÷':
            if self.calculator_screen.get_button_availability('÷'):
                self.extend_expression_with_button_text('÷', 3)
                self.calculator_screen.set_background_down_value('÷')
        elif text == '!' or text == '%':
            if self.calculator_screen.get_button_availability(text):
                self.extend_expression_with_button_text(text, 2)
                self.calculator_screen.set_background_down_value(text)
        elif text == '(':
            if self.calculator_screen.get_button_availability(text):
                self.extend_expression_with_button_text(text, 8)
                self.calculator_screen.set_background_down_value(text)
        elif text == ')':
            if self.calculator_screen.get_button_availability(text):
                self.extend_expression_with_button_text(text, 9)
                self.calculator_screen.set_background_down_value(text)
        elif text in 'pet':
            if self.calculator_screen.get_button_availability(text):
                self.extend_expression_with_button_text(text, 6)
                self.calculator_screen.set_background_down_value(text)

    def highlight_expression_error(self, items, error_info):
        error_pos = error_info[0]
        error_group = error_info[1]
        pos = 0
        while pos < len(items):
            if '.' in list(items[pos]):
                item_parts = items[pos].split('.')
                items[pos] = '{0},{1}'.format(item_parts[0], item_parts[1])
            pos += 1
        actions = ['+', '−', '×', '÷', '^']
        if error_group == 1:
            open_brackets_to_left = 0
            open_brackets_to_right = 0
            pos = error_pos + 1
            while pos < len(items):
                if items[pos] == '(':
                    open_brackets_to_right += 1
                elif items[pos] == ')':
                    if open_brackets_to_right > 0:
                        open_brackets_to_right -= 1
                    elif open_brackets_to_right == 0:
                        items[pos - 1] += '|'
                        break
                if items[pos] in actions and open_brackets_to_right == 0:
                    items[pos - 1] += '|'
                    break
                elif pos == len(items) - 1 and open_brackets_to_right == 0:
                    items[pos] += '|'
                    break
                pos += 1
            if items[error_pos] == '÷':
                while True:
                    if pos < len(items) - 1 and items[pos] == '^':
                        items[pos - 1] = items[pos - 1].split('|')[0]
                        pos += 1
                        while pos < len(items):
                            if items[pos] == '(':
                                open_brackets_to_right += 1
                            elif items[pos] == ')':
                                if open_brackets_to_right > 0:
                                    open_brackets_to_right -= 1
                                elif open_brackets_to_right == 0:
                                    items[pos - 1] += '|'
                                    break
                            if items[pos] in actions and \
                                    open_brackets_to_right == 0:
                                items[pos - 1] += '|'
                                break
                            elif pos == len(items) - 1 and \
                                    open_brackets_to_right == 0:
                                items[pos] += '|'
                                break
                            pos += 1
                    else:
                        break
            pos = error_pos - 1
            while pos >= 0:
                if items[pos] == ')':
                    open_brackets_to_left += 1
                elif items[pos] == '(':
                    if open_brackets_to_left > 0:
                        open_brackets_to_left -= 1
                    elif open_brackets_to_left == 0:
                        items[pos + 1] = '|' + items[pos + 1]
                        break
                if items[pos] in actions and open_brackets_to_left == 0:
                    if items[pos] == '−' and items[error_pos] == '^':
                        items[pos] = '|' + items[pos]
                    else:
                        items[pos + 1] = '|' + items[pos + 1]
                    break
                elif pos == 0 and open_brackets_to_left == 0:
                    items[pos] = '|' + items[pos]
                    break
                pos -= 1
            if items[error_pos] == '÷':
                while True:
                    if pos >= 0 and items[pos] == '^':
                        items[pos + 1] = items[pos + 1].split('|')[1]
                        pos -= 1
                        while pos >= 0:
                            if items[pos] == ')':
                                open_brackets_to_left += 1
                            elif items[pos] == '(':
                                if open_brackets_to_left > 0:
                                    open_brackets_to_left -= 1
                                elif open_brackets_to_left == 0:
                                    items[pos + 1] = '|' + items[pos + 1]
                                    break
                            if items[pos] in actions and \
                                    open_brackets_to_left == 0:
                                if items[pos] == '−' and \
                                        items[error_pos] == '^':
                                    items[pos] = '|' + items[pos]
                                else:
                                    items[pos + 1] = '|' + items[pos + 1]
                                break
                            elif pos == 0 and open_brackets_to_left == 0:
                                items[pos] = '|' + items[pos]
                                break
                            pos -= 1
                    else:
                        break
            elif items[error_pos] == '^':
                while True:
                    if pos >= 0 and items[pos] == '^':
                        items[pos + 1] = items[pos + 1].split('|')[1]
                        pos -= 1
                        while pos >= 0:
                            if items[pos] == ')':
                                open_brackets_to_left += 1
                            elif items[pos] == '(':
                                if open_brackets_to_left > 0:
                                    open_brackets_to_left -= 1
                                elif open_brackets_to_left == 0:
                                    items[pos + 1] = '|' + items[pos + 1]
                                    break
                            if items[pos] in actions and \
                                    open_brackets_to_left == 0:
                                if items[pos] == '−' and \
                                        items[error_pos] == '^':
                                    items[pos] = '|' + items[pos]
                                else:
                                    items[pos + 1] = '|' + items[pos + 1]
                                break
                            elif pos == 0 and open_brackets_to_left == 0:
                                items[pos] = '|' + items[pos]
                                break
                            pos -= 1
                    else:
                        break
        elif error_group == 2:
            open_brackets = 0
            pos = error_pos
            items[pos] += '|'
            pos -= 1
            while pos >= 0:
                if items[pos] == ')':
                    open_brackets += 1
                elif items[pos] == '(':
                    if open_brackets > 0:
                        open_brackets -= 1
                    elif open_brackets == 0:
                        items[pos + 1] = '|' + items[pos + 1]
                        break
                if items[pos] in actions and open_brackets == 0:
                    items[pos + 1] = '|' + items[pos + 1]
                    break
                elif pos == 0 and open_brackets == 0:
                    items[pos] = '|' + items[pos]
                    break
                pos -= 1
            if items[pos] == '−':
                items[pos + 1] = items[pos + 1].split('|')[1]
                if pos == 0 or pos > 0 and items[pos - 1] == '(':
                    items[pos] = '|' + items[pos]
        elif error_group == 3:
            open_brackets = 0
            pos = error_pos
            items[pos] = '|' + items[pos]
            pos += 1
            while pos < len(items):
                if items[pos] == '(':
                    open_brackets += 1
                elif items[pos] == ')':
                    if open_brackets > 0:
                        open_brackets -= 1
                    elif open_brackets == 0:
                        items[pos - 1] += '|'
                        break
                if items[pos] in actions and open_brackets == 0:
                    items[pos - 1] += '|'
                    break
                elif pos == len(items) - 1 and open_brackets == 0:
                    items[pos] += '|'
                    break
                pos += 1
        elif error_group == 4:
            open_brackets = 1
            pos = error_pos
            items[pos] = '|' + items[pos]
            pos += 2
            while pos < len(items):
                if items[pos] == '(':
                    open_brackets += 1
                elif items[pos] == ')':
                    if open_brackets > 0:
                        open_brackets -= 1
                    elif open_brackets == 0:
                        items[pos - 1] += '|'
                        break
                if items[pos] in actions and open_brackets == 0:
                    items[pos - 1] += '|'
                    break
                elif pos == len(items) - 1 and open_brackets == 0:
                    items[pos] += '|'
                    break
                pos += 1
        expression = ''
        for item in items:
            expression += item
        self.calculator_screen.highlight_expression(expression)

    def set_output_font_based_on_language(self):
        if self.language == 'Ελληνική':
            self.calculator_screen.set_font(1)
        elif self.language == '中国':
            self.calculator_screen.set_font(2)
        elif self.language == '日本語':
            self.calculator_screen.set_font(3)
        else:
            self.calculator_screen.set_font(0)

    def change_current_error_text_language(self):
        if self.current_error is not None:
            cause = self.current_error_cause
            self.current_error = get_error_text(self.language, cause)
            self.calculator_screen.clear_display()
            self.set_output_font_based_on_language()
            self.calculator_screen.show_output(self.current_error, False)

    def get_result_of_math_expression(self):
        expression = ''
        for text in self.texts_displayed_in_expression:
            if text == ',':
                expression += '.'
            else:
                expression += text

        items = parse_expression(expression)
        level_1 = ExpressionLevel(self.language, items.copy())
        result = level_1.get_result()

        if result is None:
            result_str = str(level_1.error)
            if level_1.error_group == 0:
                self.current_error_cause = 'overflow'
            else:
                self.current_error_cause = items[level_1.error_pos]
            error_info = [level_1.error_pos, level_1.error_group]
            self.highlight_expression_error(items, error_info)
            self.set_output_font_based_on_language()
            self.current_result = None
            self.current_error = result_str
            self.success = False
        else:
            result = result[0]
            if int(result) == result:
                result_str = str(int(result))
            else:
                result_str = str(result)
                items = result_str.split('.')
                if len(items) == 2:
                    result_str = items[0] + ',' + items[1]
            items = result_str.split('-')
            if len(items) > 1:
                result_str = ''
                for item in items:
                    result_str += item
                    result_str += '-'
            if result_str[-1] == '-':
                result_str = result_str[:-1]
            if 'e' in list(result_str):
                result_str = convert_e_type_to_decimal(result_str)
            self.current_result = result_str
            self.current_error = None
            self.current_error_cause = None
            self.success = True

        self.calculator_screen.show_output(result_str, self.success)

        self.calculator_screen.disable_equals_button()

    def push_result_text_back_to_expression(self):
        texts = list(self.current_result)
        self.do_operations_for_clear_button_press()
        for text in texts:
            if text == ',':
                self.extend_expression_with_button_text(text, 4)
            else:
                self.extend_expression_with_button_text(text, 1)

    def copy_current_output_to_clipboard(self):
        current_output = None
        if self.current_result is not None:
            items = self.current_result.split('−')
            if len(items) > 1:
                self.current_result = ''
                for item in items:
                    self.current_result += item
                    self.current_result += '-'
            if self.current_result[-1] == '-':
                self.current_result = self.current_result[:-1]
            current_output = self.current_result

        elif self.current_error is not None:
            current_output = self.current_error

        if self.running_on_desktop:
            import clipboard
            clipboard.copy(current_output)
        else:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(current_output)

    def on_request_close(self, **kwargs):
        if self.running_on_desktop:
            self.keyboard_queue.stop_analyzing()
            from kivy.config import Config
            Config.set('graphics', 'width', Window.width)
            Config.set('graphics', 'height', Window.height)
            Config.write()
        return False


def convert_e_type_to_decimal(result_str):
    result_items = result_str.split('-')
    result_str = ''
    size = int(result_items[-1]) - 1
    result_is_less_than_zero = False
    if result_items[0] == '':
        value = result_items[1].split(',')[0]
        result_is_less_than_zero = True
    else:
        value = result_items[0].split(',')[0]
    if list(value)[-1] == 'e':
        value = value[:-1]
    iteration = 0
    if result_is_less_than_zero:
        result_str += '-'
    result_str += '0,'
    while iteration < size:
        result_str += '0'
        iteration += 1
    result_str += value
    return result_str
