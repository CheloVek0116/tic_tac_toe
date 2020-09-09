import os
import json

from kivymd.uix.button import MDFlatButton
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from src.player import PlayerBase
from src.screens.end_game_dialog import EndGameDialog


class ScreenMixin(Screen):
    kv_file = None

    def __init__(self, **kwargs):
        self.set_dirs()
        kv_dir = self.dirs.get('kv_dir')
        kv_file = os.path.join(kv_dir, self.kv_file)
        if kv_file not in Builder.files:
            Builder.load_file(kv_file)
        super().__init__(**kwargs)

    def set_dirs(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        self.dirs = json.loads(app.config.get('dirs', 'defaults'))


class GameMixin(ScreenMixin):
    kv_file = 'game_mixin.kv'

    winner = None
    player = None
    opponent = None
    _players = (player, opponent)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._field = [Button(text='', ids={'id': point_id}, on_press=self.point_click) for point_id in range(9)]

        for point in self._field:
            self.ids['field_grid'].add_widget(point)

    def drop_state(self):
        for player in self._players:
            player.clear_score()
            if player.name == 'X' and not player.is_attacker:
                self.switch_attacker()
        self.ids['attacker_text'].text = 'Ходит Х'
        self.ids['score_text'].text = 'X  0:0  O'

    def switch_attacker(self):
        for player in self._players:
            player.switch_attacker()

    def is_right_move(self, point_id: int):
        is_empty_point = not bool(self._field[int(point_id)].text)
        return is_empty_point

    def point_click(self, instance: Button):
        point_id = instance.ids.get('id')
        if not self.is_right_move(point_id=point_id):
            return {}

        state = {
            'set': self.attacker.name,
            'point': point_id
        }
        self.update_state(state)
        return state

    def update_state(self, state: dict):
        self._field[state.get('point')].text = state.get('set')
        self.check_win()
        self.switch_attacker()
        self.set_attacker_text()

    def set_attacker_text(self):
        NotImplementedError()

    def update_score(self):
        x_score = self.player.get_score() if self.player.name == 'X' else self.opponent.get_score()
        o_score = self.player.get_score() if self.player.name == 'O' else self.opponent.get_score()
        self.ids['score_text'].text = f'X  {x_score} : {o_score}  O'

    def check_nobody_win(self):
        if all([point.text for point in self._field]):
            self.dialog = EndGameDialog(
                title='Ничья',
                text='Продолжить?',
                buttons=[
                    MDFlatButton(
                        text="Нет",
                        on_press=self.not_continue_game
                    ),
                    MDFlatButton(
                        text="Да",
                        on_press=self.continue_game
                    ),
                ],
            )
            self.dialog.open()

    def check_win(self):
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
            if (self._field[comb[0]].text == self._field[comb[1]].text
                    == self._field[comb[2]].text == self.attacker.name):
                self.winner = self.attacker
                break

        if self.winner:
            self.dialog = EndGameDialog(
                title=f'Выйграл "{self.winner.name}"',
                text='Продолжить?',
                buttons=[
                    MDFlatButton(
                        text="Нет",
                        on_press=self.not_continue_game
                    ),
                    MDFlatButton(
                        text="Да",
                        on_press=self.continue_game
                    ),
                ],
            )
            self.dialog.open()
            self.winner.add_point_to_score()
            self.winner = None
            self.update_score()
        else:
            self.check_nobody_win()

    def not_continue_game(self, *args):
        self.stop()

    def continue_game(self, *args):
        self.clear_field()
        self.dialog.close()
        self.dialog = None

    def clear_field(self):
        for i in range(9):
            self._field[i].text = ''

    def stop(self):
        if self.dialog:
            self.dialog.close()
            self.dialog = None

        self.clear_field()
        self.drop_state()
        self.manager.current = 'game_menu'

    @property
    def attacker(self) -> PlayerBase:
        for player in self._players:
            if player.is_attacker:
                return player
