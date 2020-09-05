__version__ = '0.4'

import uuid

from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

sm = ScreenManager()

Builder.load_file('./screens.kv')


class Player:
    def __init__(self, name: str, attacker: bool, pid: str = uuid.uuid4(), score: int = 0):
        self.id = pid
        self.name: str = name
        self._attacker: bool = attacker
        self._score: bool = score

    @property
    def is_attacker(self):
        return self._attacker

    def switch_attacker(self):
        self._attacker = not self._attacker

    def get_score(self) -> int:
        return self._score

    def add_point_to_score(self):
        self._score += 1

    def remove_point_from_score(self):
        self._score -= 1

    def __str__(self) -> str:
        return self.name


class MenuScreen(Screen):
    pass


class GameMenuScreen(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        self._field = ['' for _ in range(9)]
        self._finish: bool = False
        self.XPlayer: Player = Player(name='X', attacker=True)
        self.OPlayer: Player = Player(name='O', attacker=False)
        self._players = (self.XPlayer, self.OPlayer)
        self.winner: Player = None
        super().__init__(*args, **kwargs)

    def switch_attacker(self):
        for player in self._players:
            player.switch_attacker()

    def point_click(self, instance):
        if self._finish:
            self.clear_field()
            self._finish = False
            self.ids['attacker_text'].text = f'Ходит "{self.attacker}"'
            return

        btn_id = instance.ids['id']
        if (not self._field[int(btn_id)]
                and not self.winner
                and not all(self._field)):
            instance.text = self.attacker.name
            self._field[int(btn_id)] = self.attacker.name
            self.check_win(btn_id)
            self.switch_attacker()
            if not self.winner and not all(self._field):
                self.ids['attacker_text'].text = f'Ходит "{self.attacker}"'
        if self.winner:
            self.ids['attacker_text'].text = f'Выйграл "{self.winner}"\nТыкни на любую клетку'
            self.winner.add_point_to_score()
            self.winner = None
            self._finish = True
        elif all(self._field):
            for player in self._players:
                player.remove_point_from_score()
            self.ids['attacker_text'].text = 'Ничья\nТыкни на любую клетку'
            self.winner = None
            self._finish = True

        self.update_score()

    def update_score(self):
        self.ids['score_text'].text = f'X  {self.XPlayer.get_score()} : {self.OPlayer.get_score()}  O'

    def check_win(self, point_id):
        win_combinations = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            (2, 4, 6),
            (0, 4, 8),
        )

        for comb in win_combinations:
            if (self._field[comb[0]] == self._field[comb[1]]
                    == self._field[comb[2]] == self.attacker.name):
                self.winner = self.attacker
                break

    def clear_field(self):
        for i in range(len(self._field)):
            self._field[i] = ''
            self.ids['field_grid'].children[i].text = ''

    @property
    def attacker(self) -> Player:
        for player in self._players:
            if player.is_attacker:
                return player


class XVSOApp(MDApp):
    def build(self):
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameMenuScreen(name='game_menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm


XVSOApp().run()
