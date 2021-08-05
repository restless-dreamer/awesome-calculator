from kivy.uix.screenmanager import Screen
from calculator.standard_widgets.standard_scroll_view import StandardScrollView


class StandardScreen(Screen):
    def __init__(self, scroll_y, **kwargs):
        Screen.__init__(self, **kwargs)
        self.scroll_y = scroll_y
        for child in self.children:
            if isinstance(child, StandardScrollView):
                child.bind(scroll_y=self.on_scroll_y)
                child.scroll_y = self.scroll_y
                break
            self.get_children(child)

    def get_children(self, parent):
        for child in parent.children:
            if isinstance(child, StandardScrollView):
                child.bind(scroll_y=self.on_scroll_y)
                child.scroll_y = self.scroll_y
                break
            self.get_children(child)

    def on_scroll_y(self, *args):
        self.scroll_y = args[1]
