from calculator.screens.language_screen import LanguageScreen
from calculator.screens.theme_screen import ThemeScreen
from config_checker import get_settings_path
from absolute_path import absolute_path

language_vars = ['Português', 'Español', 'English',
                 'Français', 'Nederlands', 'Deutsch',
                 'Italiano', 'Dansk', 'Svenska',
                 'Česky', 'Slovenski', 'Polski',
                 'Magyar', 'Slovenská', 'Ελληνική',
                 'Românesc', 'Suomalainen', 'Latviešu',
                 'Lietuviškas', 'Eesti', 'Українська',
                 'Български', 'Русский', '中国', '日本語']

color_vars = ['red', 'pink', 'purple', 'deep_purple',
              'indigo', 'blue', 'light_blue', 'cyan',
              'teal', 'green', 'light_green', 'lime',
              'yellow', 'amber', 'orange', 'deep_orange',
              'brown', 'grey', 'blue_grey']

orientation_vars = ['light', 'dark']


def read_settings(settings_file):
    settings_file = absolute_path(settings_file)
    file = open(settings_file, 'r', encoding='utf8')
    lines = file.readlines()
    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos].split('\n')[0]
        pos += 1
    pos = 0
    settings = {
        'language': None,
        'language_scroll_y': None,
        'color': None,
        'orientation': None,
        'theme_scroll_y': None
    }
    while pos < len(lines):
        if lines[pos] == '[localization]':
            try:
                settings['language'] = \
                    lines[pos + 1].split(' ')[-1]
            except IndexError:
                settings['language'] = None
            try:
                settings['language_scroll_y'] = \
                    float(lines[pos + 2].split(' ')[-1])
            except (IndexError, ValueError):
                settings['language_scroll_y'] = None
            pos += 2
        elif lines[pos] == '[theme]':
            try:
                settings['color'] = \
                    lines[pos + 1].split(' ')[-1]
            except IndexError:
                settings['color'] = None
            try:
                settings['orientation'] = \
                    lines[pos + 2].split(' ')[-1]
            except IndexError:
                settings['orientation'] = None
            try:
                settings['theme_scroll_y'] = \
                    float(lines[pos + 3].split(' ')[-1])
            except (IndexError, ValueError):
                settings['theme_scroll_y'] = None
            pos += 3
        pos += 1
    file.close()
    return settings


class CalculatorSettings:
    def __init__(self, calculator_engine):
        self.calculator_engine = calculator_engine
        self.screens = []

        self.language = None
        self.language_scroll_y = None

        self.color = None
        self.orientation = None
        self.theme_scroll_y = None

        settings = read_settings(get_settings_path())
        self.assign_settings(settings)

        self.check_settings()

    def assign_settings(self, settings):
        self.language = settings['language']
        self.language_scroll_y = settings['language_scroll_y']
        self.color = settings['color']
        self.orientation = settings['orientation']
        self.theme_scroll_y = settings['theme_scroll_y']

    def check_settings(self):
        settings = read_settings('default_settings.ini')
        if self.language_scroll_y is None:
            self.language_scroll_y = settings['language_scroll_y']
        if self.theme_scroll_y is None:
            self.theme_scroll_y = settings['theme_scroll_y']
        if self.language not in language_vars:
            self.language = settings['language']
        if self.language_scroll_y < 0 or self.theme_scroll_y > 1:
            self.language_scroll_y = settings['language_scroll_y']
        if self.color not in color_vars:
            self.color = settings['color']
        if self.orientation not in orientation_vars:
            self.orientation = settings['orientation']
        if self.theme_scroll_y < 0 or self.theme_scroll_y > 1:
            self.theme_scroll_y = settings['theme_scroll_y']

    def add_screen(self, screen):
        self.screens.append(screen)

    def save(self):
        self.language = self.calculator_engine.language
        for screen in self.screens:
            if isinstance(screen, LanguageScreen):
                self.language_scroll_y = screen.scroll_y
            elif isinstance(screen, ThemeScreen):
                self.color = screen.color
                self.orientation = screen.orientation
                self.theme_scroll_y = screen.scroll_y
        localization = '[localization]\n' \
                       'language = {0}\n' \
                       'scroll_y = {1}\n'.format(self.language,
                                                 self.language_scroll_y)
        theme = '[theme]\n' \
                'color = {0}\n' \
                'orientation = {1}\n' \
                'scroll_y = {2}\n'.format(self.color,
                                          self.orientation,
                                          self.theme_scroll_y)
        settings = '{0}\n{1}\n'.format(localization, theme)
        file = open(get_settings_path(), 'w', encoding='utf8')
        file.write(settings)
        file.close()
