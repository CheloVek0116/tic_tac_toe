
from src.internet.discovery_protocol import PORT_NO
from src.internet.network import Networking
from src.player import OnlinePlayer
from src.screens.mixins import GameMixin


class OnlineGameScreen(GameMixin):
    _network: Networking = None

    def drop_state(self):
        super().drop_state()
        self.player = None
        self.opponent = None
        self._players = (None, None)

        if self._network:
            self._network.read_running = False
            self._network = None

    def stop(self):
        if self._network:
            self._send_quit()
        super().stop()

    def is_right_move(self, point_id):
        is_empty_point = super().is_right_move(point_id)
        i_is_attacker = self.attacker.id == self.player.id
        return is_empty_point and i_is_attacker

    def point_click(self, *args):
        state = super().point_click(*args)
        if state:
            state = {
                'id': self.player.id,
                **state
            }
            self._send_game_state(state)

    def set_attacker_text(self):
        who_step = "Вы" if self.attacker.id == self.player.id else "Соперник"
        self.ids['attacker_text'].text = f'Ходит {self.attacker.name}({who_step})'

    def _send_quit(self):
        self._network.send_json({
            'action': 'quit'
        }, self.opponent.remote_addr)

    def _send_game_state(self, state: dict):
        self._network.send_json({
            'action': 'state',
            'state': state
        }, self.opponent.remote_addr)

    def _on_remote_message(self, data):
        action = data['action']
        if action == 'state':
            self.update_state(data['state'])
        elif action == 'quit':
            self.stop()

    def set_settings(self, player: OnlinePlayer, opponent: OnlinePlayer):
        self.player = player
        self.opponent = opponent
        self._players = (self.player, self.opponent)

        self._network = Networking(PORT_NO)
        self._network.bind()
        self._network.run_reader_thread(self._on_remote_message)

        self.set_attacker_text()
