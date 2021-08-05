from kivy.uix.screenmanager import Screen
from calculator.special_widgets.calculator_button import CalculatorButton
from kivy.metrics import dp, sp


class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.bind(size=self.on_size)
        self.running_on_desktop = None
        self.highlight_effect = None
        self.expression_to_highlight = None
        self.output_to_highlight = None
        self.show_result_as_success = None
        self.default_background_normal = None
        self.ids.expression_label.bind(texture_size=self.on_texture_size)
        self.ids.expression_label.bind(font_size=self.on_font_size)
        self.ids.output_scroll_view.bind(scroll_x=self.on_scroll_x)
        for str_id in self.ids:
            if isinstance(self.ids[str_id], CalculatorButton):
                self.ids[str_id].bind(size=self.on_calculator_button_size)
        self.under_resizing = False
        self.current_scroll_x = 0
        self.reset_scroll_x = False

    def disable_all_calculator_buttons(self):
        for str_id in self.ids:
            if isinstance(self.ids[str_id], CalculatorButton):
                self.ids[str_id].disabled = True

    def enable_all_calculator_buttons(self):
        for str_id in self.ids:
            if isinstance(self.ids[str_id], CalculatorButton):
                self.ids[str_id].disabled = False

    def refresh_calculator_buttons(self):
        for str_id in self.ids:
            if isinstance(self.ids[str_id], CalculatorButton) \
                    and self.ids[str_id].disabled:
                self.ids[str_id].disabled = False
                self.ids[str_id].disabled = True

    def on_calculator_button_size(self, *args):
        if self.running_on_desktop:
            args[0].font_size = sp(int((args[0].width +
                                        args[0].height) / 6))
        else:
            args[0].font_size = sp(int((args[0].width +
                                        args[0].height) / 16))

    def basic_calculator_buttons_disablement(self):
        self.enable_all_calculator_buttons()

        self.ids.comma_button.disabled = True
        self.ids.equals_button.disabled = True
        self.ids.plus_button.disabled = True
        self.ids.multiply_button.disabled = True
        self.ids.divide_button.disabled = True
        self.ids.power_button.disabled = True
        self.ids.factorial_button.disabled = True
        self.ids.percent_button.disabled = True
        self.ids.bracket_2_button.disabled = True
        self.ids.erase_button.disabled = True
        self.ids.clear_button.disabled = True

    def calculator_button_of_group_1_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.number_0_button.disabled = False
        self.ids.number_1_button.disabled = False
        self.ids.number_2_button.disabled = False
        self.ids.number_3_button.disabled = False
        self.ids.number_4_button.disabled = False
        self.ids.number_5_button.disabled = False
        self.ids.number_6_button.disabled = False
        self.ids.number_7_button.disabled = False
        self.ids.number_8_button.disabled = False
        self.ids.number_9_button.disabled = False

        self.ids.comma_button.disabled = False
        self.ids.equals_button.disabled = False
        self.ids.plus_button.disabled = False
        self.ids.minus_button.disabled = False
        self.ids.multiply_button.disabled = False
        self.ids.divide_button.disabled = False
        self.ids.power_button.disabled = False
        self.ids.factorial_button.disabled = False
        self.ids.percent_button.disabled = False
        self.ids.bracket_2_button.disabled = False
        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def calculator_button_of_group_2_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.equals_button.disabled = False
        self.ids.plus_button.disabled = False
        self.ids.minus_button.disabled = False
        self.ids.multiply_button.disabled = False
        self.ids.divide_button.disabled = False
        self.ids.power_button.disabled = False
        self.ids.factorial_button.disabled = False
        self.ids.percent_button.disabled = False
        self.ids.bracket_2_button.disabled = False
        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def calculator_button_of_group_3_pressed(self):
        self.enable_all_calculator_buttons()

        self.ids.comma_button.disabled = True
        self.ids.equals_button.disabled = True
        self.ids.plus_button.disabled = True
        self.ids.minus_button.disabled = True
        self.ids.multiply_button.disabled = True
        self.ids.divide_button.disabled = True
        self.ids.power_button.disabled = True
        self.ids.factorial_button.disabled = True
        self.ids.percent_button.disabled = True
        self.ids.bracket_2_button.disabled = True

    def calculator_button_of_group_4_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.number_0_button.disabled = False
        self.ids.number_1_button.disabled = False
        self.ids.number_2_button.disabled = False
        self.ids.number_3_button.disabled = False
        self.ids.number_4_button.disabled = False
        self.ids.number_5_button.disabled = False
        self.ids.number_6_button.disabled = False
        self.ids.number_7_button.disabled = False
        self.ids.number_8_button.disabled = False
        self.ids.number_9_button.disabled = False

        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def calculator_button_of_group_5_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.number_0_button.disabled = False
        self.ids.number_1_button.disabled = False
        self.ids.number_2_button.disabled = False
        self.ids.number_3_button.disabled = False
        self.ids.number_4_button.disabled = False
        self.ids.number_5_button.disabled = False
        self.ids.number_6_button.disabled = False
        self.ids.number_7_button.disabled = False
        self.ids.number_8_button.disabled = False
        self.ids.number_9_button.disabled = False
        self.ids.bracket_1_button.disabled = False
        self.ids.const_p_button.disabled = False
        self.ids.const_e_button.disabled = False
        self.ids.const_t_button.disabled = False
        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def calculator_button_of_group_6_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.equals_button.disabled = False
        self.ids.plus_button.disabled = False
        self.ids.minus_button.disabled = False
        self.ids.multiply_button.disabled = False
        self.ids.divide_button.disabled = False
        self.ids.power_button.disabled = False
        self.ids.factorial_button.disabled = False
        self.ids.percent_button.disabled = False
        self.ids.bracket_2_button.disabled = False
        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def calculator_button_of_group_7_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.bracket_1_button.disabled = False
        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def calculator_button_of_group_8_pressed(self):
        self.enable_all_calculator_buttons()

        self.ids.comma_button.disabled = True
        self.ids.equals_button.disabled = True
        self.ids.plus_button.disabled = True
        self.ids.multiply_button.disabled = True
        self.ids.divide_button.disabled = True
        self.ids.power_button.disabled = True
        self.ids.factorial_button.disabled = True
        self.ids.percent_button.disabled = True
        self.ids.bracket_2_button.disabled = True

    def calculator_button_of_group_9_pressed(self):
        self.disable_all_calculator_buttons()

        self.ids.equals_button.disabled = False
        self.ids.plus_button.disabled = False
        self.ids.minus_button.disabled = False
        self.ids.multiply_button.disabled = False
        self.ids.divide_button.disabled = False
        self.ids.power_button.disabled = False
        self.ids.factorial_button.disabled = False
        self.ids.percent_button.disabled = False
        self.ids.bracket_2_button.disabled = False
        self.ids.erase_button.disabled = False
        self.ids.clear_button.disabled = False

    def on_texture_size(self, *args):
        if args[1][0] >= self.width - dp(20):
            args[0].font_size -= 1

    def on_font_size(self, *args):
        if args[0].texture_size[0] < self.width - dp(20) and \
                args[1] < sp(30):
            args[0].font_size += 1

    def set_comfortable_font_size(self):
        if self.ids.expression_label.texture_size[0] >= \
                self.width - dp(20):
            self.ids.expression_label.font_size -= 1
        elif self.ids.expression_label.font_size < sp(30):
            self.ids.expression_label.font_size += 1

    def add_to_displaying_text(self, text):
        self.ids.expression_label.text += text

    def remove_from_displaying_text(self, text):
        self.ids.expression_label.text = \
            self.ids.expression_label.text[:-len(text)]

    def clear_displaying_text(self):
        self.ids.expression_label.text = ''

    def get_button_availability(self, text):
        value = None
        if text == '0':
            value = self.ids.number_0_button.disabled
        elif text == '1':
            value = self.ids.number_1_button.disabled
        elif text == '2':
            value = self.ids.number_2_button.disabled
        elif text == '3':
            value = self.ids.number_3_button.disabled
        elif text == '4':
            value = self.ids.number_4_button.disabled
        elif text == '5':
            value = self.ids.number_5_button.disabled
        elif text == '6':
            value = self.ids.number_6_button.disabled
        elif text == '7':
            value = self.ids.number_7_button.disabled
        elif text == '8':
            value = self.ids.number_8_button.disabled
        elif text == '9':
            value = self.ids.number_9_button.disabled
        elif text == ',':
            value = self.ids.comma_button.disabled
        elif text == '=':
            value = self.ids.equals_button.disabled
        elif text == '+':
            value = self.ids.plus_button.disabled
        elif text == '−':
            value = self.ids.minus_button.disabled
        elif text == '×':
            value = self.ids.multiply_button.disabled
        elif text == '÷':
            value = self.ids.divide_button.disabled
        elif text == '^':
            value = self.ids.power_button.disabled
        elif text == '!':
            value = self.ids.factorial_button.disabled
        elif text == '%':
            value = self.ids.percent_button.disabled
        elif text == '(':
            value = self.ids.bracket_1_button.disabled
        elif text == ')':
            value = self.ids.bracket_2_button.disabled
        elif text == 'p':
            value = self.ids.const_p_button.disabled
        elif text == 'e':
            value = self.ids.const_e_button.disabled
        elif text == 't':
            value = self.ids.const_t_button.disabled
        elif text == 'E':
            value = self.ids.erase_button.disabled
        elif text == 'C':
            value = self.ids.clear_button.disabled
        return not value

    def set_background_normal_by_default(self):
        for str_id in self.ids:
            if isinstance(self.ids[str_id], CalculatorButton) and \
                    self.ids[str_id].background_normal == \
                    self.ids[str_id].background_down:
                self.ids[str_id].background_normal = \
                    self.default_background_normal

    def set_background_down_value(self, text):
        if text == '0':
            self.ids.number_0_button.background_normal = \
                self.ids.number_0_button.background_down
        elif text == '1':
            self.ids.number_1_button.background_normal = \
                self.ids.number_1_button.background_down
        elif text == '2':
            self.ids.number_2_button.background_normal = \
                self.ids.number_2_button.background_down
        elif text == '3':
            self.ids.number_3_button.background_normal = \
                self.ids.number_3_button.background_down
        elif text == '4':
            self.ids.number_4_button.background_normal = \
                self.ids.number_4_button.background_down
        elif text == '5':
            self.ids.number_5_button.background_normal = \
                self.ids.number_5_button.background_down
        elif text == '6':
            self.ids.number_6_button.background_normal = \
                self.ids.number_6_button.background_down
        elif text == '7':
            self.ids.number_7_button.background_normal = \
                self.ids.number_7_button.background_down
        elif text == '8':
            self.ids.number_8_button.background_normal = \
                self.ids.number_8_button.background_down
        elif text == '9':
            self.ids.number_9_button.background_normal = \
                self.ids.number_9_button.background_down
        elif text == ',':
            self.ids.comma_button.background_normal = \
                self.ids.comma_button.background_down
        elif text == '=':
            self.ids.equals_button.background_normal = \
                self.ids.equals_button.background_down
        elif text == '+':
            self.ids.plus_button.background_normal = \
                self.ids.plus_button.background_down
        elif text == '−':
            self.ids.minus_button.background_normal = \
                self.ids.minus_button.background_down
        elif text == '×':
            self.ids.multiply_button.background_normal = \
                self.ids.multiply_button.background_down
        elif text == '÷':
            self.ids.divide_button.background_normal = \
                self.ids.divide_button.background_down
        elif text == '^':
            self.ids.power_button.background_normal = \
                self.ids.power_button.background_down
        elif text == '!':
            self.ids.factorial_button.background_normal = \
                self.ids.factorial_button.background_down
        elif text == '%':
            self.ids.percent_button.background_normal = \
                self.ids.percent_button.background_down
        elif text == '(':
            self.ids.bracket_1_button.background_normal = \
                self.ids.bracket_1_button.background_down
        elif text == ')':
            self.ids.bracket_2_button.background_normal = \
                self.ids.bracket_2_button.background_down
        elif text == 'p':
            self.ids.const_p_button.background_normal = \
                self.ids.const_p_button.background_down
        elif text == 'e':
            self.ids.const_e_button.background_normal = \
                self.ids.const_e_button.background_down
        elif text == 't':
            self.ids.const_t_button.background_normal = \
                self.ids.const_t_button.background_down
        elif text == 'E':
            self.ids.erase_button.background_normal = \
                self.ids.erase_button.background_down
        elif text == 'C':
            self.ids.clear_button.background_normal = \
                self.ids.clear_button.background_down

    def enable_bracket_2_button(self):
        self.ids.bracket_2_button.disabled = False

    def disable_bracket_2_button(self):
        self.ids.bracket_2_button.disabled = True

    def disable_equals_button(self):
        self.ids.equals_button.disabled = True

    def enable_equals_button(self):
        self.ids.equals_button.disabled = False

    def disable_number_buttons(self):
        self.ids.number_0_button.disabled = True
        self.ids.number_1_button.disabled = True
        self.ids.number_2_button.disabled = True
        self.ids.number_3_button.disabled = True
        self.ids.number_4_button.disabled = True
        self.ids.number_5_button.disabled = True
        self.ids.number_6_button.disabled = True
        self.ids.number_7_button.disabled = True
        self.ids.number_8_button.disabled = True
        self.ids.number_9_button.disabled = True

    def disable_comma_button(self):
        self.ids.comma_button.disabled = True

    def enable_comma_button(self):
        self.ids.comma_button.disabled = False

    def set_highlight_effect(self, highlight_color):
        self.highlight_effect = '[color={0}]'.format(highlight_color)

    def update_highlighted_expression(self):
        if self.expression_to_highlight is not None:
            self.highlight_expression(self.expression_to_highlight)

    def highlight_expression(self, expression):
        expression_items = expression.split('|')
        if len(expression_items) > 1:
            highlighted_expression = expression_items[0] + \
                                     self.highlight_effect + \
                                     expression_items[1] + \
                                     '[/color]' + expression_items[2]
        else:
            highlighted_expression = self.highlight_effect + \
                                     expression_items[0] + '[/color]'
        self.ids.expression_label.text = highlighted_expression
        self.expression_to_highlight = expression

    def stop_expression_highlighting(self):
        if self.expression_to_highlight is not None:
            expression_items = self.expression_to_highlight.split('|')
            default_expression = ''
            for expression_item in expression_items:
                default_expression += expression_item
            self.ids.expression_label.text = default_expression
            self.expression_to_highlight = None

    def set_font(self, font_id):
        font_name = None
        if font_id == 0:
            font_name = 'fonts/nunito_regular.ttf'
        elif font_id == 1:
            font_name = 'fonts/open_sans_regular.ttf'
        elif font_id == 2:
            font_name = 'fonts/zcool_xiaowei_regular.ttf'
        elif font_id == 3:
            font_name = 'fonts/shippori_mincho_medium.ttf'
        self.ids.output_label.font_name = font_name

    def update_highlighted_output(self):
        if self.output_to_highlight is not None:
            output = self.output_to_highlight
            output = self.highlight_output(output)
            self.ids.output_label.text = output

    def highlight_output(self, output_str):
        output_items = output_str.split('|')
        if len(output_items) == 3:
            highlighted_output = output_items[0] + \
                                 self.highlight_effect + \
                                 output_items[1] + \
                                 '[/color]' + output_items[2]
            output_items = highlighted_output.split('@')
            if len(output_items) == 3:
                highlighted_output = output_items[0] + \
                                     '[font=fonts/nunito_regular.ttf]' + \
                                     output_items[1] + \
                                     '[/font]' + output_items[2]
            self.output_to_highlight = output_str
            return highlighted_output
        return output_str

    def show_output(self, output_str, success):
        output = self.highlight_output(output_str)
        self.show_result_as_success = success
        self.ids.output_label.text = output
        if success:
            self.ids.output_scroll_view.width = self.width - dp(74)
            self.ids.output_cover_layout.right = self.width - dp(74)
            self.ids.push_button.width = dp(24)
            self.ids.copy_button.width = dp(24)
        else:
            self.ids.output_scroll_view.width = self.width - dp(40)
            self.ids.output_cover_layout.right = self.width - dp(40)
            self.ids.copy_button.width = dp(24)
        self.reset_scroll_x = True

    def clear_display(self):
        font_name = 'fonts/nunito_regular.ttf'
        self.ids.expression_label.font_size = sp(30)
        self.output_to_highlight = None
        self.ids.output_label.font_name = font_name
        self.ids.output_label.text = ''
        self.ids.output_label.width = 0
        self.ids.output_scroll_view.scroll_x = 0
        self.ids.push_button.width = 0
        self.ids.copy_button.width = 0

    def show_extended_calculator_buttons(self):
        self.ids.extended_calculator_buttons_layout.come_in()

    def hide_extended_calculator_buttons(self):
        self.ids.extended_calculator_buttons_layout.come_out()

    def update_scroll_view(self, success):
        if success:
            self.ids.output_scroll_view.width = self.width - dp(74)
            self.ids.output_cover_layout.right = self.width - dp(74)
            self.ids.output_scroll_view.scroll_x = self.current_scroll_x
            if self.ids.output_label.width + dp(74) <= self.width:
                self.ids.output_scroll_view.scroll_x = 0
        else:
            self.ids.output_scroll_view.width = self.width - dp(40)
            self.ids.output_cover_layout.right = self.width - dp(40)
            self.ids.output_scroll_view.scroll_x = self.current_scroll_x
            if self.ids.output_label.width + dp(40) <= self.width:
                self.ids.output_scroll_view.scroll_x = 0

    def on_scroll_x(self, *args):
        if not self.under_resizing:
            self.current_scroll_x = args[1]
            if self.current_scroll_x > 1:
                self.current_scroll_x = 1
        if self.reset_scroll_x:
            self.ids.output_scroll_view.scroll_x = 0
            self.current_scroll_x = 0
            self.reset_scroll_x = False

    def on_size(self, *args):
        self.under_resizing = True
        self.update_scroll_view(self.show_result_as_success)
        self.set_comfortable_font_size()
        if self.running_on_desktop:
            if dp(args[1][0]) > dp(550):
                self.show_extended_calculator_buttons()
            else:
                self.hide_extended_calculator_buttons()

        if not self.running_on_desktop:
            if args[1][0] > args[1][1]:
                self.show_extended_calculator_buttons()
            else:
                self.hide_extended_calculator_buttons()
        self.under_resizing = False
