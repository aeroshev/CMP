from argparse import ArgumentParser

from .handlers_check import CheckOutputFile, CheckServerKey, CheckStringKey, GetResult

from cmp.grammar import Parser
from cmp.helpers import LogMixin, Singleton


class Command(ArgumentParser, LogMixin, Singleton):
    """
    CLI interface class
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._chain_responsibility = CheckServerKey()
        self._chain_responsibility.set_next(
            CheckStringKey()
        ).set_next(
            CheckOutputFile()
        ).set_next(
            GetResult()
        )
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
        """
        Entry point of program CMP
        for executed in command line
        """
        args = self.parse_args()
        parser = self._get_parser()
        setattr(args, 'parser', parser)
        setattr(args, 'matlab_ast', None)

        output = self._chain_responsibility.handle(args)
        if output:
            self.logger.info(output)

    @staticmethod
    def _get_parser() -> Parser:
        return Parser(yacc_debug=False)
