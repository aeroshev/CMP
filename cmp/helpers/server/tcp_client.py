import asyncio
import os
from argparse import ArgumentParser, Namespace
from typing import Optional


class TCPClient(ArgumentParser):
    """Simple TCP client for sending in MATLAB compiler"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.address = os.environ.get("HOSTNAME", '127.0.0.1')
        self.port = os.environ.get("PORT", 8888)
        self.description = 'TCP client for server MATLAB compiler'
        self.command_group = self.add_mutually_exclusive_group(required=True)
        self.command_group.add_argument(
            '-d',
            '--data',
            type=str,
            help='input data for compiler from console'
        )
        self.command_group.add_argument(
            '-f',
            '--file',
            type=str,
            help='input data for compiler from file'
        )
        self.add_argument(
            '-p',
            '--port',
            required=False,
            type=int,
            help='Port of connection server'
        )
        self.add_argument(
            '-a',
            '--address',
            required=False,
            type=str,
            help='Address of connection server'
        )

    def execute(self) -> None:
        args = self.parse_args()

        message = self._get_text(args)
        address = self.address
        if args.address:
            address = args.address
        port = self.port
        if args.port:
            port = args.port

        print(args)

        response = asyncio.run(self._send_data(message, address, port))
        print(response)

    @staticmethod
    def _validate_file(path: str) -> bool:
        return os.path.isfile(path)

    def _get_text(self, args: Namespace) -> Optional[str]:
        if args.data:
            return str(args.data)
        else:
            if not self._validate_file(args.file):
                print('Incorrect path file')
                return None
            with open(args.file, "r") as file:
                content = file.read()
            return content

    @staticmethod
    async def _send_data(message: str, host: str, port: int) -> str:
        reader, writer = await asyncio.open_connection(host, port)
        print(message)
        writer.write(message.encode())
        print('Send')
        data = await reader.read(100)
        writer.close()

        return data.decode(encoding='utf-8')


if __name__ == '__main__':
    client = TCPClient()
    client.execute()
