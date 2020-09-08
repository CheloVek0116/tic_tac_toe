from src.player import Player
from src.screens.mixins import GameMixin


class GameScreen(GameMixin):
    player = Player('X', True)
    opponent = Player('O', False)
    _players = (player, opponent)

    def set_attacker_text(self):
        self.ids['attacker_text'].text = f'Ходит {self.attacker.name}'
