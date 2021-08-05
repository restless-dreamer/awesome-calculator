import config_checker

config_checker.check_configurations()

if __name__ == '__main__':
    from kivy.lang import Builder
    from absolute_path import absolute_path
    from initialize_window import initialize_window
    from calculator.calculator_engine import CalculatorEngine

    layout_file = absolute_path('user_interface.kv')
    with open(layout_file, 'r', encoding='utf8') as kv:
        Builder.load_string(kv.read())
    calculator_engine = CalculatorEngine()
    initialize_window(calculator_engine)
    calculator_engine.run()
