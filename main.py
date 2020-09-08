"""
XVSO app
"""
__version__ = '0.5'


from kivymd.app import MDApp

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from src.screens import (
    GameMenuScreen,
    GameScreen,
    MenuScreen,
    OnlineGameScreen,
    OnlineLoadingScreen,
)

Builder.load_file('./screens.kv')


class XVSOApp(MDApp):
    """
    Главный модуль приложения
    """
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(MenuScreen(name='menu'))
        screen_manager.add_widget(GameMenuScreen(name='game_menu'))
        screen_manager.add_widget(OnlineLoadingScreen(name='online_loading'))
        screen_manager.add_widget(GameScreen(name='game'))
        screen_manager.add_widget(OnlineGameScreen(name='online_game'))
        return screen_manager


XVSOApp().run()
