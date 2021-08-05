import os
from kivy.config import Config
from kivy.utils import platform
from absolute_path import absolute_path


def get_settings_path():
    settings = None
    home = os.path.expanduser('~')
    if platform == 'win':
        app_data = os.path.join(home, 'AppData', 'Local')
        rd_dir = os.path.join(app_data, 'Restless Dreamer')
        my_dir = os.path.join(rd_dir, 'Awesome Calculator')
        settings = os.path.join(my_dir, 'settings.ini')
    elif platform == 'linux':
        rd_dir = os.path.join(home, '.restlessdreamer')
        my_dir = os.path.join(rd_dir, 'Awesome Calculator')
        settings = os.path.join(my_dir, 'settings.ini')
    elif platform == 'android':
        my_dir = os.getcwd()
        settings = os.path.join(my_dir, 'settings.ini')
    return settings


def check_configurations():
    if platform == 'win' or platform == 'linux':
        rd_dir, my_dir = None, None
        config, settings = None, None
        home = os.path.expanduser('~')
        if platform == 'win':
            app_data = os.path.join(home, 'AppData', 'Local')
            rd_dir = os.path.join(app_data, 'Restless Dreamer')
            my_dir = os.path.join(rd_dir, 'Awesome Calculator')
            config = os.path.join(my_dir, 'config.ini')
            settings = os.path.join(my_dir, 'settings.ini')
        elif platform == 'linux':
            rd_dir = os.path.join(home, '.restlessdreamer')
            my_dir = os.path.join(rd_dir, 'Awesome Calculator')
            config = os.path.join(my_dir, 'config.ini')
            settings = os.path.join(my_dir, 'settings.ini')
        if os.path.exists(rd_dir):
            if os.path.exists(my_dir):
                if os.path.exists(config):
                    Config.read(config)
                else:
                    copy_config(config)
                    Config.read(config)
                if not os.path.exists(settings):
                    copy_settings(settings)
            else:
                os.mkdir(my_dir)
                copy_configurations(config, settings)
        else:
            os.makedirs(my_dir)
            copy_configurations(config, settings)
    elif platform == 'android':
        my_dir = os.getcwd()
        settings = os.path.join(my_dir, 'settings.ini')
        if not os.path.exists(settings):
            copy_settings(settings)


def copy_configurations(config, settings):
    copy_config(config)
    copy_settings(settings)
    Config.read(config)


def copy_config(config):
    name = None
    if platform == 'win':
        name = 'windows.ini'
    elif platform == 'linux':
        name = 'linux.ini'
    path = absolute_path('default_config/' + name)
    config_0 = open(path, 'r', encoding='utf8')
    config_1 = open(config, 'w', encoding='utf8')
    config_1.writelines(config_0.readlines())
    config_1.close()
    config_0.close()


def copy_settings(settings):
    path = absolute_path('default_settings.ini')
    settings_0 = open(path, 'r', encoding='utf8')
    settings_1 = open(settings, 'w', encoding='utf8')
    settings_1.writelines(settings_0.readlines())
    settings_1.close()
    settings_0.close()
