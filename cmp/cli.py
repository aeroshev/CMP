import os
from argparse import ArgumentParser
from pkg_resources import require as pkg_require

from cmp.grammar import Parser
from cmp.helpers import LogMixin, Singleton
from cmp.traverse import Visitor


class Command(ArgumentParser, LogMixin, Singleton):
    """
    CLI interface class
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.description = 'Empty description'
        self.add_argument(
            '-p',
            '--path',
            required=True,
            type=str,
            help='path to file'
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
            version=f'Pycmp {pkg_require("pycmp")[0].version}'
        )

    def execute(self) -> None:
        args = self.parse_args()

        if not self._validate_file(args.path):
            self.logger.error("Incorrect path to file")
            return None

        parser = self._get_parser()

        ast = parser.parse(text=self._get_text_file(args.path), debug_level=False)

        if args.output_file:
            if not self._validate_file(args.output_file):
                self.logger.error("Incorrect path to file")
                return None
            visitor = self._get_visitor(filename=args.output_file)
        else:
            visitor = self._get_visitor(filename='')

        visitor.traverse_ast(root=ast, use_file=True)

    @staticmethod
    def _validate_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def _get_parser() -> Parser:
        return Parser(yacc_debug=False)

    @staticmethod
    def _get_visitor(filename: str) -> Visitor:
        if filename:
            return Visitor(filename=filename)
        else:
            return Visitor()

    @staticmethod
    def _get_text_file(path: str) -> str:
        with open(path, "r") as file:
            content = file.read()
        return content
