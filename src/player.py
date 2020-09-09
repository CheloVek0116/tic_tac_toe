import uuid


class PlayerBase:
    def __init__(self, name: str, attacker: bool):
        self.name = name
        self._attacker = attacker
        self._score = 0

    @property
    def is_attacker(self) -> bool:
        return self._attacker

    def switch_attacker(self):
        self._attacker = not self._attacker

    def get_score(self) -> int:
        return self._score

    def add_point_to_score(self):
        self._score += 1

    def remove_point_from_score(self):
        self._score -= 1

    def clear_score(self):
        self._score = 0

    def __str__(self) -> str:
        return self.name


class Player(PlayerBase):
    pass


class OnlinePlayer(PlayerBase):
    def __init__(self, name: str, attacker: bool, pid: str = str(uuid.uuid4()), remote_addr: str = ''):
        super().__init__(name, attacker)
        self.id = pid
        self.remote_addr = remote_addr

    def __str__(self):
        return f'{self.name} player {self.id}({self._remote_addr})'
