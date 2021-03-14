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
        primary_expression : IDENTIFIER
                           | CONSTANT
                           | STRING_LITERAL
                           | '(' expression ')'
                           | '[' ']'
                           | '[' array_list ']'
        """

    def p_postfix_expression(self, p):
        """
        postfix_expression : primary_expression
                           | array_expression
                           | postfix_expression TRANSPOSE
                           | postfix_expression NCTRANSPOSE
        """

    def p_index_expression(self, p):
        """
        index_expression : ':'
                         | expression
        """

    def p_index_expression_list(self, p):
        """
        index_expression_list : index_expression
                              | index_expression_list ',' index_expression
        """

    def p_array_expression(self, p):
        """
        array_expression : IDENTIFIER '(' index_expression_list ')'
        """

    def p_unary_expression(self, p):
        """
        unary_expression : postfix_expression
                         | unary_operator postfix_expression
        """

    def p_unary_operator(self, p):
        """
        unary_operator : '+'
                       | '-'
                       | '~'
        """

    def p_multiplicative_expression(self, p):
        """
        multiplicative_expression : unary_expression
                                  | multiplicative_expression '*' unary_expression
                                  | multiplicative_expression '/' unary_expression
                                  | multiplicative_expression '\\' unary_expression
                                  | multiplicative_expression '^' unary_expression
                                  | multiplicative_expression ARRAY_MUL unary_expression
                                  | multiplicative_expression ARRAY_DIV unary_expression
                                  | multiplicative_expression ARRAY_RDIV unary_expression
                                  | multiplicative_expression ARRAY_POW unary_expression
        """

    def p_additive_expression(self, p):
        """
        additive_expression : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative_expression
        """

    def p_relational_expression(self, p):
        """
        relational_expression : additive_expression
                              | relational_expression '<' additive_expression
                              | relational_expression '>' additive_expression
                              | relational_expression LE_OP additive_expression
                              | relational_expression GE_OP additive_expression
        """

    def p_equality_expression(self, p):
        """
        equality_expression : relational_expression
                            | equality_expression EQ_OP relational_expression
                            | equality_expression NE_OP relational_expression
        """

    def p_and_expression(self, p):
        """
        and_expression : equality_expression
                       | and_expression '&' equality_expression
        """

    def p_or_expression(self, p):
        """
        or_expression : and_expression
                      | or_expression '|' and_expression
        """

    def p_expression(self, p):
        """
        expression : or_expression
                   | expression ':' or_expression
        """

    def p_assignment_expression(self, p):
        """
        assignment_expression : postfix_expression '=' expression
        """

    def p_eostmt(self, p):
        """
        eostmt : ','
               | ';'
               | CR
        """

    def p_statement(self, p):
        """
        statement : global_statement
                  | clear_statement
                  | assignment_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement
        """

    def p_statement_list(self, p):
        """
        statement_list : statement
                       | statement_list statement
        """

    def p_identifier_list(self, p):
        """
        identifier_list : IDENTIFIER
                        | identifier_list IDENTIFIER
        """

    def p_global_statement(self, p):
        """
        global_statement : GLOBAL identifier_list eostmt
        """

    def p_clear_statement(self, p):
        """
        clear_statement : CLEAR identifier_list eostmt
        """

    def p_expression_statement(self, p):
        """
        expression_statement : eostmt
                             | expression eostmt
        """

    def p_assignment_statement(self, p):
        """
        assignment_statement : assignment_expression eostmt
        """

    def p_array_element(self, p):
        """
        array_element : expression
                      | expression_statement
        """

    def p_array_list(self, p):
        """
        array_list : array_element
                   | array_list array_element
        """

    def p_selection_statement(self, p):
        """
        selection_statement : IF expression statement_list END eostmt
                            | IF expression statement_list ELSE statement_list END eostmt
                            | IF expression statement_list elseif_clause END eostmt
                            | IF expression statement_list elseif_clause ELSE statement_list END eostmt
        """

    def p_elseif_clause(self, p):
        """
        elseif_clause : ELSEIF expression statement_list
                      | elseif_clause ELSEIF expression statement_list
        """

    def p_iteration_statement(self, p):
        """
        iteration_statement : WHILE expression statement_list END eostmt
                            | FOR IDENTIFIER '=' expression statement_list END eostmt
                            | FOR '(' IDENTIFIER '=' expression ')' statement_list END eostmt
        """

    def p_jump_statement(self, p):
        """
        jump_statement : BREAK eostmt
                       | RETURN eostmt
        """

    def p_translation_unit(self, p):
        """
        translation_unit : statement_list
                         | FUNCTION func_declare eostmt statement_list
        """

    def p_func_identifier_list(self, p):
        """
        func_return_list : IDENTIFIER
                         | func_identifier_list ',' IDENTIFIER
        """

    def p_func_return_list(self, p):
        """
        func_return_list : IDENTIFIER
                         | '[' func_identifier_list ']'
        """

    def p_func_declare_lhs(self, p):
        """
        func_declare_lhs : IDENTIFIER
                         | IDENTIFIER '(' ')'
                         | IDENTIFIER '(' func_identifier_list ')'
        """

    def p_func_declare(self, p):
        """
        func_declare : func_declare_lhs
                     | func_return_list '=' func_declare_lhs
        """

    def p_error(self, p):
        print(f"Syntax error in input! {p}")


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
