import asyncio
import os
from abc import ABC, abstractmethod
from argparse import Namespace
from functools import partial
from typing import Optional

from pycmp.grammar import Parser
from pycmp.helpers import BadInputError, LogMixin
from pycmp.helpers.server import TCPServer
from pycmp.traverse.traverse_ast import Visitor


class Handler(ABC):
    """Base handler without subject area"""
    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        ...

    @abstractmethod
    def handle(self, args: Namespace) -> Optional[str]:
        ...


class AbstractHandler(Handler, LogMixin):
    """Abstract handler for CLI interface CMP"""
    _next_handler = None  # type: Handler

    @staticmethod
    def _validate_file(path: str) -> bool:
        return os.path.isfile(path)

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, args: Namespace) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(args)
        return None


class CheckServerKey(AbstractHandler):
    """
    Check server option in input stream.
    If key -S/--server is true, TCP server
    will be started
    """
    @staticmethod
    def network_execute(message: str, parser: Parser) -> Optional[str]:
        """
        Special entry point of program CMP
        for working in TCP server
        """
        if message:
            matlab_ast = parser.parse(text=message, debug_level=False)
        else:
            output = 'Incorrect input data'
            return output

        if parser.has_errors:
            output = '\n'.join([msg for msg in parser.errors()])
        else:
            visitor = Visitor()
            try:
                output = visitor.traverse_ast(root=matlab_ast) or 'Nothing'
            except BadInputError as err:
                output = str(err)

        parser.flush_errors()
        return output

    def handle(self, args: Namespace) -> Optional[str]:
        if args.server:
            parser = args.parser
            keys = {
                'host': args.host,
                'port': args.port,
                'consumer': partial(self.network_execute, parser=parser)
            }
            tcp_server = TCPServer(**keys)
            try:
                tcp_server.execute()
            except KeyboardInterrupt:
                self.logger.info("Server shutdown")
            return None
        else:
            return super().handle(args)


class CheckStringKey(AbstractHandler):
    """
    Check -s/--string and -p/--path key in input stream.
    Only one of two keys expected.
    If --string is true, data will get from input stream.
    If --path is true, data will read from file by directed path
    """
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

    def handle(self, args: Namespace) -> Optional[str]:
        text = self._get_text(args)
        if text:
            matlab_ast = args.parser.parse(text=self._get_text(args), debug_level=False)
            setattr(args, 'matlab_ast', matlab_ast)
            return super().handle(args)
        else:
            self.logger.error('Incorrect input data')
            return None


class CheckOutputFile(AbstractHandler):
    """
    Check -of/--output-file key.
    If it is true, result data will write in file by directed file.
    In default result show in output stream
    """
    def handle(self, args: Namespace) -> Optional[str]:
        if args.output_file:
            if not self._validate_file(args.output_file):
                self.logger.error("Incorrect output path to file")
                return None
        return super().handle(args)


class GetResult(AbstractHandler):
    """
    After checks all keys this class
    generated result
    """
    @staticmethod
    def _get_visitor(filename: str = None) -> Visitor:
        if filename:
            return Visitor(filename=filename)
        else:
            return Visitor()

    def handle(self, args: Namespace) -> Optional[str]:
        visitor = self._get_visitor(filename=args.output_file)
        try:
            output = visitor.traverse_ast(root=args.matlab_ast)
            return output
        except BadInputError as err:
            self.logger.error(err)
            return None
