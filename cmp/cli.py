import asyncio
import os
from argparse import ArgumentParser, Namespace
from typing import Optional

from cmp.grammar import Parser
from cmp.helpers import BadInputError, LogMixin, Singleton
from cmp.helpers.server import TCPServer
from cmp.traverse import Visitor


class Command(ArgumentParser, LogMixin, Singleton):
    """
    CLI interface class
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.description = 'Compiler MATLAB code to Python scripts'
        self.command_group = self.add_mutually_exclusive_group(required=True)
        self.command_group.add_argument(
            '-p',
            '--path',
            type=str,
            help='path to file'
        )
        self.command_group.add_argument(
            '-s',
            '--string',
            type=str,
            help='input data from console'
        )
        self.command_group.add_argument(
            '-S',
            '--server',
            action='store_true',
            help='Run async TCP server'
        )
        self.add_argument(
            '-of',
            '--output-file',
            required=False,
            type=str,
            help='path to output file'
        )
        self.add_argument(
            '-v',
            '--version',
            action='version',
            version='Pycmp: 1.0.0'
        )
        self.add_argument(
            '-P',
            '--port',
            required=False,
            type=int,
            help='Port of server'
        )
        self.add_argument(
            '-H',
            '--host',
            required=False,
            type=str,
            help='Hostname of server'
        )

    def execute(self) -> None:
        args = self.parse_args()
        parser = self._get_parser()

        if args.server:
            keys = {
                'host': args.host,
                'port': args.port,
                'consumer': self.network_execute
            }
            tcp_server = TCPServer(**keys)
            try:
                asyncio.run(tcp_server.execute())
            except KeyboardInterrupt:
                self.logger.info("Server shutdown")
                return None

        text = self._get_text(args)
        if text:
            ast = parser.parse(text=self._get_text(args), debug_level=False)
        else:
            self.logger.error('Incorrect input data')
            return None

        if args.output_file:
            if not self._validate_file(args.output_file):
                self.logger.error("Incorrect output path to file")
                return None

        visitor = self._get_visitor(filename=args.output_file)
        try:
            output = visitor.traverse_ast(root=ast)
        except BadInputError as err:
            self.logger.error(err)
            return None

        if output:
            self.logger.info(output)

    def network_execute(self, message: str) -> Optional[str]:
        parser = self._get_parser()
        if message:
            ast = parser.parse(text=message, debug_level=False)
        else:
            self.logger.error('Incorrect input data')
            return None

        visitor = Visitor()
        try:
            output = visitor.traverse_ast(root=ast)
        except BadInputError as err:
            self.logger.error(err)
            return None

        return output

    @staticmethod
    def _validate_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def _get_parser() -> Parser:
        return Parser(yacc_debug=False)

    @staticmethod
    def _get_visitor(filename: str = None) -> Visitor:
        if filename:
            return Visitor(filename=filename)
        else:
            return Visitor()

    def _get_text(self, args: Namespace) -> Optional[str]:
        if args.string:
            return str(args.string)
        else:
            if not self._validate_file(args.path):
                self.logger.error('Incorrect path file')
                return None
            with open(args.path, "r") as file:
                content = file.read()
                return content
