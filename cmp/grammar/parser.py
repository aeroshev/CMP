import logging

import ply.yacc as yacc

from lexer import Lexer


logger = logging.getLogger()


class Parser:
    def __init__(
            self,
            lexer=Lexer,
            yacc_debug=True,
            tab_out_put_dir=''
    ):
        self.lex = lexer()
        self.tokens = self.lex.tokens
        self.parser = yacc.yacc(
            module=self,
            start='primary_expression',
            debug=yacc_debug,
            outputdir=tab_out_put_dir,
            optimize=1
        )
        self._scope_stack = [dict()]
        self._last_yielded_token = None
        self._err_flag = False

    def parse(self, text, filename='', debug_level=True):
        return self.parser.parse(
            input=text,
            lexer=self.lex,
            debug=logger
        )

    def p_primary_expression(self, p):
        """
        primary_expression : ID
        """
        p[0] = p[1]
    #
    # def p_expression(self, p):
    #     """
    #     expression : or_expression
    #                | expression
    #     """
    #     p[0] = p[1]


    def p_error(self, p):
        print("Syntax error in input!")


data = '''
if (a == 245)
    do_something
else
    to_do



% Just a comment
'''


if __name__ == '__main__':
    parser = Parser(yacc_debug=True)
    parser.parse(text=data, debug_level=False)
