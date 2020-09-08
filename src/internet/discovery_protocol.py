import logging
import threading
import uuid

from src.internet.network import Networking

PORT_NO = 37020


class DiscoveryProtocol:
    A_DISCOVERY = 'discovery'
    A_STOP_SCAN = 'stop_scan'

    VALID_ACTIONS = [A_DISCOVERY, A_STOP_SCAN]

    def __init__(self, pid: str):
        assert pid
        self._my_pid = pid
        self._network = Networking(PORT_NO, broadcast=True)
        self._network.bind()

    def _send_action(self, action: str, data: dict = None):
        """
        Форматирует JSON для обмена командами
        :param action: имя команды
        :param data: доп. данные, если надо
        :return:
        """
        data = data if data else {}
        self._network.send_json_broadcast({'action': action, 'sender': self._my_pid, **data})

    def _is_message_for_me(self, data: dict) -> bool:
        """
        Проверяет, относится ли принятый пакет к нашему протоколу обнаружения
        (1) должен быть определнный action
        (2) отправитель sender должен быть не я, а кто-то другой, потому что
            мы также получаем собственные пакеты)
        :param data: словарь данных
        :return: bool
        """
        return data and data.get('action') in self.VALID_ACTIONS and data.get('sender') != self._my_pid

    def run(self):
        while True:
            logging.info('Scanning...')
            # рассылаем всем сообщение A_DISCOVERY
            self._send_action(self.A_DISCOVERY)

            # ждем приемлемого ответа не более 5 секунд, игнорируя таймауты и неревалентные пакеты
            raw_data = self._network.recv_json_until(self._is_message_for_me, timeout=5.0)
            data = raw_data.get('data')
            addr = raw_data.get('address')

            # если пришло что-то наше
            if data:
                action, sender = data['action'], data['sender']
                # кто-то нам отправил A_DISCOVERY
                if action == self.A_DISCOVERY:
                    # отсылаем ему сообщение остановить сканирование A_STOP_SCAN, указав его PID
                    self._send_action(self.A_STOP_SCAN, {'to_pid': sender})
                    # todo: что делать, если оно не дошло? тот пир продолжит сканировать дальше...
                elif action == self.A_STOP_SCAN:
                    # если получили сообщение остановить сканирование, нужно выяснить нам ли оно предназначено
                    if data['to_pid'] != self._my_pid:
                        continue  # это не нам; игнорировать!
                return addr, sender

    def run_in_background(self, callback: callable):
        """
        Ищет соперника в фоне и вызывает callback
        :param callback:
        :return:
        """
        def await_with_callback():
            results = self.run()
            callback(*results)
        threading.Thread(target=await_with_callback, daemon=True).start()


if __name__ == '__main__':
    print('Testing the discovery protocol.')
    pid = str(uuid.uuid4())
    print('pid =', pid)
    info = DiscoveryProtocol(pid).run()
    print("success: ", info)
