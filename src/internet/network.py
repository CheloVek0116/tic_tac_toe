import json
import logging
import socket
import threading
import time


class Networking:
    BUFFER_SIZE = 4096  # размер буфера для примем сообщений
    TIME_OUT = 1.0  # время таймаута при ожидании данных в сокет

    def __init__(self, port_no, broadcast=False):
        self.read_running = False
        self.port_no = port_no
        self._socket = self.get_socket(broadcast=broadcast)

    @classmethod
    def get_socket(cls, broadcast: bool = False, timeout: int = TIME_OUT) -> socket.socket:
        """
        Создает UDP сокет
        :param broadcast: широковещателньый или нет
        :param timeout: тайм аут
        :return: сокет
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # чтобы на одной машине можно было слушать тотже порт
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        if broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)
        return sock

    def recv_json(self) -> dict:
        """
        Получить JSON из сокета
        :return: dict
        """
        try:
            # получить датаграмму и адрес из сокета
            data, addr = self._socket.recvfrom(self.BUFFER_SIZE)
            # декодируем в юникод и загружаем из JSON
            return {
                'data': json.loads(data.decode('utf-8', errors='ignore'), encoding='utf-8'),
                'address': addr
            }
        except json.JSONDecodeError:
            logging.error('JSONDecodeError!')
        except socket.timeout:
            pass  # ничего не пришло
        return {}

    def recv_json_until(self, predicate: callable, timeout: int) -> dict:
        """
        Несколько раз пытается получить JSON в течение timeout секунд, пока на полученных данных
        функция predicate не вернет True
        :param predicate: функция, чтобы проверять данные
        :param timeout: тайм аут
        :return:
        """
        t0 = time.monotonic()
        while time.monotonic() < t0 + timeout:
            raw_data = self.recv_json()
            data = raw_data.get('data')
            addr = raw_data.get('address')
            if predicate(data):
                return {
                    'data': data,
                    'address': addr
                }
        return {}

    def run_reader_thread(self, callback: callable):
        """
        Запускает отдельный поток, чтобы получать данные из сокета
        :param callback: функция, которая вызывается, если получены данные
        """
        self.read_running = True

        def reader_job():
            while self.read_running:
                raw_data = self.recv_json()
                if raw_data:
                    data = raw_data['data']
                    callback(data)

        # daemon=True, чтобы не зависал, если выйдет основной поток
        thread = threading.Thread(target=reader_job, daemon=True)
        thread.start()
        return thread

    def bind(self, to: str = ""):
        """
        Привязаться к порту, то есть начать слушать с него сообщения
        После bind можно вызывать recv_json
        :param to: интерфейс ("" - любой)
        """
        self._socket.bind((to, self.port_no))

    def send_json(self, data: dict, to):
        """
        Отправляет JSON
        :param data: данные
        :param to: адрес кому отправить
        """
        data = bytes(json.dumps(data), 'utf-8')
        return self._socket.sendto(data, (to, self.port_no))

    def send_json_broadcast(self, data: dict):
        """
        Оправляет JSON данные широковещательно
        :param data: данные
        :return:
        """
        return self.send_json(data, "<broadcast>")

    def __del__(self):
        logging.info('Closing socket')
        self._socket.close()
