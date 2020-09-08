from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen

from src.internet.discovery_protocol import DiscoveryProtocol
from src.player import OnlinePlayer


class OnlineLoadingScreen(Screen):
    discovery = None
    player = None
    opponent = None
    game = None

    def on_enter(self, *args):
        self.player = OnlinePlayer(name='', attacker=False)
        self.scan()

    def scan(self):
        # начать сканирование, если еще не начато
        if not self.discovery:
            self.discovery = DiscoveryProtocol(self.player.id)
            self.discovery.run_in_background(self.on_found_peer)

    @mainthread
    def on_found_peer(self, addr, opponent_id):
        print(f'Найден соперник {opponent_id}@{addr}')
        self.discovery = None

        self.game = self.manager.get_screen('online_game')
        self.opponent = OnlinePlayer(name='', attacker=False, pid=opponent_id, remote_addr=addr[0])

        my_id_sum = sum([int(s) for s in self.player.id if s.isdigit()])
        opponent_id_sum = sum([int(s) for s in opponent_id if s.isdigit()])
        is_attacker = opponent_id_sum < my_id_sum
        if is_attacker:
            self.player.name = 'X'
            self.player.switch_attacker()

            self.opponent.name = 'O'
        else:
            self.player.name = 'O'

            self.opponent.name = 'X'
            self.opponent.switch_attacker()

        self.game.set_settings(self.player, self.opponent)

        self.game = None
        self.player = None
        self.opponent = None

        # перейти на окно с игрой
        self.manager.current = 'online_game'
