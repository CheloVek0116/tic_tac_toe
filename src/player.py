import uuid


class PlayerBase:
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


class Player(PlayerBase):
    pass


class OnlinePlayer(PlayerBase):
    def __init__(self, name: str, attacker: bool, pid: str = str(uuid.uuid4()), remote_addr: str = ''):
        super().__init__(name, attacker)
        self.id = pid
        self._score: bool = 0
        self._remote_addr: str = remote_addr

    @property
    def remote_addr(self):
        return self._remote_addr

    def __str__(self):
        return f'{self.name} player {self.id}({self._remote_addr})'
