from kivy.uix.button import Button
from kivy.properties import NumericProperty


class CalculatorButton(Button):
    group = NumericProperty(0)
