"""
XVSO app
"""
__version__ = '0.5'

import os

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from src.screens import (
    GameMenuScreen,
    GameScreen,
    MenuScreen,
    OnlineGameScreen,
    OnlineLoadingScreen,
)


class XVSOApp(MDApp):
    """
    Главный модуль приложения
    """
    def build_config(self, config):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SOURCE_DIR = os.path.join(BASE_DIR, 'src')
        KV_DIR = os.path.join(SOURCE_DIR, 'kv')
        import json
        DIRS = {
            'defaults': json.dumps({
                "base_dir": BASE_DIR,
                "source_dir": SOURCE_DIR,
                "kv_dir": KV_DIR,
            })
        }

        config.setdefaults('dirs', DIRS)

    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(MenuScreen(name='menu'))
        screen_manager.add_widget(GameMenuScreen(name='game_menu'))
        screen_manager.add_widget(OnlineLoadingScreen(name='online_loading'))
        screen_manager.add_widget(GameScreen(name='game'))
        screen_manager.add_widget(OnlineGameScreen(name='online_game'))
        return screen_manager


if __name__ == '__main__':
    app = XVSOApp()
    app.run()
