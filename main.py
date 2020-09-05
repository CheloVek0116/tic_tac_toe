__version__ = '0.3'

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class Player:
    def __init__(self, name: str, attacker: bool):
        self.name: str = name
        self._attacker: bool = attacker
        self._score: bool = 0

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


class XVSOApp(App):
    def __init__(self, *args, **kwargs):
        self._rows: int = 3
        self._cols: int = 3
        self._field = ['' for _ in range(self._rows * self._cols)]

        self.XPlayer: Player = Player('X', True)
        self.OPlayer: Player = Player('O', False)
        self._players = (self.XPlayer, self.OPlayer)
        self.winner: Player = None

        self._finish: bool = False
        super().__init__(*args, **kwargs)

    @property
    def attacker(self) -> Player:
        for player in self._players:
            if player.is_attacker:
                return player

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=5)
        self.label = Label(text=f'Ходит "{self.attacker}"', size_hint=(1, .1), valign='middle', halign='center')
        self.score_text = Label(text=f'X  0 : 0  O', size_hint=(1, .2), font_size='20sp', valign='middle', halign='center')
        self.grid = GridLayout(cols=self._cols)
        for point_id in range(len(self._field)):
            button = Button(ids={'id': point_id},
                            on_press=self.point_click)
            self.grid.add_widget(button)

        layout.add_widget(self.score_text)
        layout.add_widget(self.label)
        layout.add_widget(self.grid)
        return layout

    def switch_attacker(self):
        for player in self._players:
            player.switch_attacker()

    def point_click(self, instance):
        if self._finish:
            self.clear_field()
            self._finish = False
            self.label.text = f'Ходит "{self.attacker}"'
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
                self.label.text = f'Ходит "{self.attacker}"'
        if self.winner:
            self.label.text = f'Выйграл "{self.winner}"\nТыкни на любую клетку'
            self.winner.add_point_to_score()
            self.winner = None
            self._finish = True
        elif all(self._field):
            for player in self._players:
                player.remove_point_from_score()
            self.label.text = 'Ничья\nТыкни на любую клетку'
            self.winner = None
            self._finish = True

        self.update_score()

    def update_score(self):
        self.score_text.text = f'X  {self.XPlayer.get_score()} : {self.OPlayer.get_score()}  O'

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
            self.grid.children[i].text = ''


XVSOApp().run()
