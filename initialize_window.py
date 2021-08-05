from kivy.core.window import Window
from kivy.metrics import dp


def initialize_window(calculator_engine):
    Window.minimum_width = dp(300)
    Window.minimum_height = dp(400)
    Window.clearcolor = [1, 1, 1, 1]
    Window.on_request_close = calculator_engine.on_request_close
