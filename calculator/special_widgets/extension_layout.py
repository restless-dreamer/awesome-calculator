from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation


class ExtensionLayout(GridLayout):
    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.extended = False

    def come_in(self):
        if not self.extended:
            self.extended = True
            animation = Animation(size_hint=[1, 1], duration=0.1)
            animation.start(self)

    def come_out(self):
        if self.extended:
            self.extended = False
            animation = Animation(size_hint=[0, 1], width=0, duration=0.1)
            animation.start(self)
