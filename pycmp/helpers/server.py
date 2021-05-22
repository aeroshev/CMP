import os
import socket
from typing import Callable

from pycmp.helpers.log import LogMixin


class TCPServer(LogMixin):
    """
    Server for service matlab compiler
    hostname - IP address or domen name local machine where is server will run
    port - the port that the server will listen to
    consumer - function what will give result str -> str
    """
    def __init__(self, consumer: Callable[[str], str], host: str = None, port: int = None) -> None:
        self.hostname = host or os.environ.get("HOSTNAME", '127.0.0.1')
        self.port = port or os.environ.get("PORT", 8888)
        self.consumer = consumer

    def execute(self) -> None:
        """Start TCP server"""
        self.logger.info(f"Start server on address {self.hostname}:{self.port}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.hostname, self.port))
        sock.listen(1)

        while True:
            try:
                conn, addr = sock.accept()
                self.logger.info(f"Receive data from {addr}")

                data = conn.recv(8192)
                response = self.consumer(data.decode(encoding='utf-8'))
                if not response:
                    response = 'Internal error'
                conn.send(response.encode(encoding='utf-8'))

                conn.close()
            except KeyboardInterrupt:
                break
        self.logger.info('Server shutdown')
