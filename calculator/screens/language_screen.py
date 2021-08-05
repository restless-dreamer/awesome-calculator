from calculator.standard_widgets.standard_screen import StandardScreen


class LanguageScreen(StandardScreen):
    def __init__(self, calculator_engine, scroll_y, **kwargs):
        StandardScreen.__init__(self, scroll_y, **kwargs)
        self.calculator_engine = calculator_engine
        self.bind(height=self.height_callback)

    def height_callback(self, *args):
        if args[1] > self.ids.language_box_layout.height:
            self.ids.language_scroll_view.size_hint = (1, None)
            self.ids.language_scroll_view.height = \
                self.ids.language_box_layout.height
        else:
            self.ids.language_scroll_view.size_hint = (1, 1)

    def set_language(self, language, initialization=False):
        if language != self.calculator_engine.language:
            self.calculator_engine.language = language
            self.calculator_engine.change_current_error_text_language()
            if not initialization:
                self.calculator_engine.settings.save()
        if not initialization:
            self.manager.current = 'calculator_screen'
