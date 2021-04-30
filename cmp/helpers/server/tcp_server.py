import asyncio
import os
from typing import Callable

from cmp.helpers import LogMixin


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

    async def execute(self) -> None:
        """Start TCP server"""
        self.logger.info(f"Start server on address {self.hostname}:{self.port}")
        print(f"Start server on address {self.hostname}:{self.port}")
        server = await asyncio.start_server(self._handle_connect, self.hostname, self.port)
        async with server:
            await server.serve_forever()

    async def _handle_connect(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        data = await reader.read()
        message = data.decode(encoding='utf-8')
        addr = writer.get_extra_info('peername')
        print(f"Received data from {addr[0]}:{addr[1]}")

        response = self.consumer(message)
        if response is None:
            response = 'Internal error'
        writer.write(response.encode())
        writer.write_eof()
        await writer.drain()

        writer.close()
        await writer.wait_closed()
