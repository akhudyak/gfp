import socket
import logging
from sensors_icd import *

class TcpClient:
    def __init__(self, name, ip, port):
        self.ip = ip
        self.port = port
        self.logger = logging.getLogger()
        self._is_connected = False
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.tcp_socket.connect((self.ip, self.port))
            self._is_connected = True
            self.logger.info(
                f"Client has been assigned socket name {self.tcp_socket.getsockname()}")
        except Exception as ex:
            self.logger.error(
                f'Failed to connect to DG server {self.ip}:{self.port} - {ex}')

    def send(self, msg, buffer):
        msg.to_bytes_array(buffer, 0)
        if (self._is_connected):
            self.tcp_socket.send(buffer)
            logging.info(f'{msg.header.message_seq_number} was sent')


class TcpServer:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.tcp_socket.bind((self.ip, self.port))
            self.tcp_socket.listen(1)
            conn, addr = self.tcp_socket.accept()
            print(f"bind to {self.ip}:{self.port}")
            return conn, addr
        except Exception as ex:
            print(
                f'exception in tcp server:{self.name} {self.ip}:{self.port} - {ex}')
