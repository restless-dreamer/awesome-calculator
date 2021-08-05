from calculator.standard_widgets.standard_screen import StandardScreen
from calculator.standard_widgets.standard_button import StandardButton
from calculator.standard_widgets.standard_label import StandardLabel
from calculator.standard_widgets.standard_scroll_view import StandardScrollView
from calculator.special_widgets.calculator_button import CalculatorButton
from calculator.screens.calculator_screen import CalculatorScreen
from calculator.special_widgets.language_button import LanguageButton
from absolute_path import absolute_path
from PIL import Image


class ThemeScreen(StandardScreen):
    def __init__(self, global_settings, scroll_y, **kwargs):
        StandardScreen.__init__(self, scroll_y, **kwargs)
        self.global_settings = global_settings
        self.screens = []
        self.color = None
        self.orientation = None

    def add_screen(self, screen):
        self.screens.append(screen)

    def set_theme(self, color, orientation):
        self.color = color
        self.orientation = orientation
        background_color = None
        if self.orientation == 'light':
            background_color = 'colors/{0}/50.png'.format(self.color)
        elif self.orientation == 'dark':
            background_color = 'colors/{0}/900.png'.format(self.color)
        for screen in self.screens:
            if not isinstance(screen, ThemeScreen):
                screen.ids.color_layout.color = background_color
                self.perform_changes_on_children(screen)
            if isinstance(screen, CalculatorScreen):
                screen.ids.output_cover_layout.color = \
                    background_color
                default_background_normal = None
                if self.orientation == 'light':
                    default_background_normal = \
                        'colors/{0}/100.png'.format(self.color)
                elif self.orientation == 'dark':
                    default_background_normal = \
                        'colors/{0}/800.png'.format(self.color)
                screen.default_background_normal = \
                    default_background_normal
                screen.refresh_calculator_buttons()
                highlight_color_file = None
                if self.orientation == 'light':
                    if color == 'deep_purple':
                        highlight_color_file = \
                            'colors/{0}/400.png'.format(self.color)
                    elif color == 'indigo':
                        highlight_color_file = \
                            'colors/{0}/400.png'.format(self.color)
                    elif color == 'blue':
                        highlight_color_file = \
                            'colors/{0}/600.png'.format(self.color)
                    elif color == 'light_blue':
                        highlight_color_file = \
                            'colors/{0}/600.png'.format(self.color)
                    elif color == 'cyan':
                        highlight_color_file = \
                            'colors/{0}/600.png'.format(self.color)
                    elif color == 'teal':
                        highlight_color_file = \
                            'colors/{0}/400.png'.format(self.color)
                    elif color == 'light_green':
                        highlight_color_file = \
                            'colors/{0}/600.png'.format(self.color)
                    elif color == 'lime':
                        highlight_color_file = \
                            'colors/{0}/700.png'.format(self.color)
                    elif color == 'yellow':
                        highlight_color_file = \
                            'colors/{0}/700.png'.format(self.color)
                    elif color == 'amber':
                        highlight_color_file = \
                            'colors/{0}/600.png'.format(self.color)
                    else:
                        highlight_color_file = \
                            'colors/{0}/500.png'.format(self.color)
                elif self.orientation == 'dark':
                    if color == 'red':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'pink':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'purple':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'deep_purple':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'indigo':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'light_blue':
                        highlight_color_file = \
                            'colors/{0}/400.png'.format(self.color)
                    elif color == 'cyan':
                        highlight_color_file = \
                            'colors/{0}/400.png'.format(self.color)
                    elif color == 'teal':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'amber':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'orange':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'deep_orange':
                        highlight_color_file = \
                            'colors/{0}/200.png'.format(self.color)
                    elif color == 'grey':
                        highlight_color_file = \
                            'colors/{0}/500.png'.format(self.color)
                    else:
                        highlight_color_file = \
                            'colors/{0}/300.png'.format(self.color)
                image = Image.open(absolute_path(highlight_color_file))
                matrix = image.load()
                r = matrix[0, 0][0]
                g = matrix[0, 0][1]
                b = matrix[0, 0][2]
                highlight_color = '%02x%02x%02x' % (r, g, b)
                screen.set_highlight_effect(highlight_color)
                screen.update_highlighted_expression()
                screen.update_highlighted_output()

    def change_theme(self, color, orientation):
        self.set_theme(color, orientation)
        self.global_settings.save()
        self.manager.current = 'calculator_screen'

    def perform_changes_on_children(self, parent):
        for child in parent.children:
            if isinstance(child, StandardButton):
                icon_color = None
                if self.orientation == 'light':
                    icon_color = 'black'
                elif self.orientation == 'dark':
                    icon_color = 'white'
                background_normal = 'background_normal/' + \
                                    child.icon_used + '.png'
                background_down = 'background_down/' + \
                                  child.icon_used + '.png'
                child.background_normal = \
                    'icons/{0}/{1}'.format(icon_color, background_normal)
                child.background_down = \
                    'icons/{0}/{1}'.format(icon_color, background_down)
            elif isinstance(child, StandardLabel):
                if self.orientation == 'light':
                    child.color = [0, 0, 0, 1]
                elif self.orientation == 'dark':
                    child.color = [1, 1, 1, 1]
            elif isinstance(child, StandardScrollView):
                if self.orientation == 'light':
                    child.bar_color = [0, 0, 0, 1]
                    child.bar_inactive_color = [0, 0, 0, 0]
                elif self.orientation == 'dark':
                    child.bar_color = [1, 1, 1, 1]
                    child.bar_inactive_color = [1, 1, 1, 0]
            elif isinstance(child, CalculatorButton):
                background_a = None
                background_b = None
                background_c = None
                if self.orientation == 'light':
                    background_a = 'colors/{0}/100.png'.format(self.color)
                    background_b = 'colors/{0}/200.png'.format(self.color)
                    background_c = 'colors/{0}/300.png'.format(self.color)
                    child.color = [0, 0, 0, 1]
                elif self.orientation == 'dark':
                    background_a = 'colors/{0}/800.png'.format(self.color)
                    background_b = 'colors/{0}/700.png'.format(self.color)
                    background_c = 'colors/{0}/600.png'.format(self.color)
                    child.color = [1, 1, 1, 1]
                child.background_normal = background_a
                child.background_down = background_b
                child.background_disabled_normal = background_c
            elif isinstance(child, LanguageButton):
                background_a = None
                background_b = None
                if self.orientation == 'light':
                    background_a = 'colors/{0}/50.png'.format(self.color)
                    background_b = 'colors/{0}/100.png'.format(self.color)
                    child.color = [0, 0, 0, 1]
                elif self.orientation == 'dark':
                    background_a = 'colors/{0}/900.png'.format(self.color)
                    background_b = 'colors/{0}/800.png'.format(self.color)
                    child.color = [1, 1, 1, 1]
                child.background_normal = background_a
                child.background_down = background_b
            self.perform_changes_on_children(child)
