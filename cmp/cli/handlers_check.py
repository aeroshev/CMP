from typing import Any, Optional
from abc import ABC, abstractmethod
from argparse import Namespace
import asyncio
from cmp.helpers.server import TCPServer


class Handler(ABC):
    """"""
    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        ...

    @abstractmethod
    def handle(self, args: Namespace) -> Optional[str]:
        ...


class AbstractHandler(Handler):
    """"""
    _next_handler = None  # type: Handler

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, args: Namespace) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(args)
        return None


class CheckServerKey(AbstractHandler):
    """"""
    def handle(self, args: Namespace) -> Optional[str]:
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
        else:
            return super().handle(args)


class CheckStringKey(AbstractHandler):
    """"""
    def handle(self, args: Namespace) -> Optional[str]:
        text = self._get_text(args)
        if text:
            ast = args.parser.parse(text=self._get_text(args), debug_level=False)
            setattr(args, 'ast', ast)
            return super().handle(args)
        else:
            self.logger.error('Incorrect input data')
            return None


class CheckOutputFile(AbstractHandler):
    """"""
    def handle(self, args: Namespace) -> Optional[str]:
        if args.output_file:
            if not self._validate_file(args.output_file):
                self.logger.error("Incorrect output path to file")
                super().handle(args)
        else:
            return None


class GetResult(AbstractHandler):
    """"""
    def handle(self, args: Namespace) -> Optional[str]:
        visitor = self._get_visitor(filename=args.output_file)
        try:
            output = visitor.traverse_ast(root=args.ast)
            return output
        except BadInputError as err:
            self.logger.error(err)
            return None


class ServerRun(AbstractHandler):
    """"""