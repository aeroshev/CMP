import os
from typing import Optional
from argparse import ArgumentParser, Namespace

from cmp.grammar import Parser
from cmp.helpers import LogMixin, Singleton, BadInputError
from cmp.traverse import Visitor


class Command(ArgumentParser, LogMixin, Singleton):
    """
    CLI interface class
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.description = 'Empty description'
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

    def execute(self) -> None:
        args = self.parse_args()
        parser = self._get_parser()
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

        output = None
        try:
            output = visitor.traverse_ast(root=ast)
        except BadInputError as err:
            # self.logger.error(err)
            print(err)

        if output:
            # self.logger.info(output)
            print(output)

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

    def _get_text(self, args: Namespace) -> Optional[str]:
        if args.string:
            return args.string
        else:
            if not self._validate_file(args.path):
                self.logger.error('Incorrect path file')
                return None
            with open(args.path, "r") as file:
                content = file.read()
            return content
