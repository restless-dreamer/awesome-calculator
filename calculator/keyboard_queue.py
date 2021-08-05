from threading import Thread
from time import sleep


class KeyboardQueue(Thread):
    def __init__(self, calculator_engine):
        Thread.__init__(self)
        self.keyboard_queue = []
        self.calculator_engine = calculator_engine
        self.calculator_screen = calculator_engine.calculator_screen
        self.stop = False

    def add_pressed_key(self, key):
        self.keyboard_queue.insert(0, key)

    def run(self):
        while True:
            if self.stop:
                break
            if len(self.keyboard_queue) > 0:
                key = self.keyboard_queue[0]
                self.calculator_engine.analyze_pressed_key(key)
                try:
                    self.keyboard_queue.pop(0)
                except IndexError:
                    pass
            else:
                sleep(0.1)
                self.calculator_screen.set_background_normal_by_default()

    def clear_keyboard_queue(self):
        self.keyboard_queue.clear()

    def stop_analyzing(self):
        self.stop = True
