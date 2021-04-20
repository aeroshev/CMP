import asyncio
import os
from typing import Callable

from cmp.helpers import LogMixin


class TCPServer(LogMixin):  # TODO setup logger write in file
    """Server for service matlab compiler"""

    def __init__(self, consumer: Callable[[str], str]) -> None:
        self.hostname = os.environ.get("HOSTNAME", '127.0.0.1')
        self.port = os.environ.get("PORT", 8888)
        self.consumer = consumer

    async def execute(self) -> None:
        self.logger.info(f"Start server on address {self.hostname}:{self.port}")
        print(f"Start server on address {self.hostname}:{self.port}")
        server = await asyncio.start_server(self._handle_connect, self.hostname, self.port)
        async with server:
            await server.serve_forever()

    async def _handle_connect(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        print('Handle connect')
        data = await reader.read()
        message = data.decode(encoding='utf-8')
        addr = writer.get_extra_info('peername')
        self.logger.info(f"Received data from {addr}")

        response = self.consumer(message)
        print(response)
        writer.write(response.encode())
        # await writer.drain()
        writer.close()
