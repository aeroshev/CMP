import os
from argparse import ArgumentParser

from cmp.grammar import Parser
from cmp.helpers import LogMixin, Singleton


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

    def execute(self) -> None:
        args = self.parse_args()

        if not self._validate_file(args.path):
            self.logger.error("Incorrect path to file")
            return None

        parser = self._get_parser()

        parser.parse(text=self._get_text_file(args.path))

    @staticmethod
    def _validate_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def _get_parser() -> Parser:
        return Parser(yacc_debug=False)

    @staticmethod
    def _get_text_file(path: str) -> str:
        with open(path, "r") as file:
            content = file.read()
        return content
