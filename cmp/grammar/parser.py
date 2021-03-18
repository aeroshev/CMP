import ply.yacc as yacc

from cmp.ast import *
from cmp.grammar import Lexer
from cmp.helpers import LogMixin


class Parser(LogMixin):
    """Executive parser object"""
    handlers = {
        "<": LowerRelationalNode,
        ">": GreaterRelationalNode,
        "LE_OP": LowerEqualRelationalNode,
        "GE_OP": GreaterEqualRelationalNode,
        "EQ_OP": PositiveEqualityNode,
        "NE_OP": NegativeEqualityNode,
        "&": AndNode,
        "|": OrNode
    }

    def __init__(
            self,
            lexer=Lexer,
            yacc_debug=True,
            tab_out_put_dir=''
    ) -> None:
        self.lex = lexer()
        self.tokens = self.lex.tokens
        self.parser = yacc.yacc(
            module=self,
            start='translation_unit',
            debug=yacc_debug,
            outputdir=tab_out_put_dir,
            optimize=1
        )
        self._scope_stack = [dict()]
        self._last_yielded_token = None
        self._err_flag = False

    def _lhs_rhs_expression(self, p: yacc.YaccProduction) -> None:
        if len(p) == 4:
            p[0] = self.handlers[p[2].type](lhs=p[1], rhs=p[3])
        else:
            p[0] = p[1]

    def parse(self, text, filename='', debug_level=True) -> Node:
        return self.parser.parsedebug(
            input=text,
            lexer=self.lex,
            debug=self.logger
        )

    def p_primary_expression(self, p: yacc.YaccProduction) -> None:
        """
        primary_expression : IDENTIFIER
                           | CONSTANT
                           | STRING_LITERAL
                           | '(' expression ')'
                           | '[' ']'
                           | '[' array_list ']'
        """
        for index, token in enumerate(p):
            if token in {'(', ')', '[', ']'}:
                p.pop(index)

        if len(p) > 1:
            p[0] = p[1]
        else:
            ...

    def p_postfix_expression(self, p: yacc.YaccProduction) -> None:
        """
        postfix_expression : primary_expression
                           | array_expression
                           | postfix_expression TRANSPOSE
        """

    def p_index_expression(self, p: yacc.YaccProduction) -> None:
        """
        index_expression : ':'
                         | expression
        """

    def p_index_expression_list(self, p: yacc.YaccProduction) -> None:
        """
        index_expression_list : index_expression
                              | index_expression_list ',' index_expression
        """

    def p_array_expression(self, p: yacc.YaccProduction) -> None:
        """
        array_expression : IDENTIFIER '(' index_expression_list ')'
        """

    def p_unary_expression(self, p: yacc.YaccProduction) -> None:
        """
        unary_expression : postfix_expression
                         | unary_operator postfix_expression
        """

    def p_unary_operator(self, p: yacc.YaccProduction) -> None:
        """
        unary_operator : '+'
                       | '-'
                       | '~'
        """

    def p_multiplicative_expression(self, p: yacc.YaccProduction) -> None:
        """
        multiplicative_expression : unary_expression
                                  | multiplicative_expression '*' unary_expression
                                  | multiplicative_expression '/' unary_expression
                                  | multiplicative_expression '^' unary_expression
                                  | multiplicative_expression ARRAY_MUL unary_expression
                                  | multiplicative_expression ARRAY_DIV unary_expression
                                  | multiplicative_expression ARRAY_RDIV unary_expression
                                  | multiplicative_expression ARRAY_POW unary_expression
        """

    def p_additive_expression(self, p: yacc.YaccProduction) -> None:
        """
        additive_expression : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative_expression
        """

    def p_relational_expression(self, p: yacc.YaccProduction) -> None:
        """
        relational_expression : additive_expression
                              | relational_expression '<' additive_expression
                              | relational_expression '>' additive_expression
                              | relational_expression LE_OP additive_expression
                              | relational_expression GE_OP additive_expression
        """
        self._lhs_rhs_expression(p)

    def p_equality_expression(self, p: yacc.YaccProduction) -> None:
        """
        equality_expression : relational_expression
                            | equality_expression EQ_OP relational_expression
                            | equality_expression NE_OP relational_expression
        """
        self._lhs_rhs_expression(p)

    def p_and_expression(self, p: yacc.YaccProduction) -> None:
        """
        and_expression : equality_expression
                       | and_expression '&' equality_expression
        """
        self._lhs_rhs_expression(p)

    def p_or_expression(self, p: yacc.YaccProduction) -> None:
        """
        or_expression : and_expression
                      | or_expression '|' and_expression
        """
        self._lhs_rhs_expression(p)

    def p_expression(self, p: yacc.YaccProduction) -> None:
        """
        expression : or_expression
                   | expression ':' or_expression
        """

    def p_assignment_expression(self, p: yacc.YaccProduction) -> None:
        """
        assignment_expression : postfix_expression '=' expression
        """
        p[0] = AssignmentNode(lhs=p[1], rhs=p[3])

    def p_eostmt(self, p: yacc.YaccProduction) -> None:
        """
        eostmt : ','
               | ';'
               | NEWLINE
        """

    def p_statement(self, p: yacc.YaccProduction) -> None:
        """
        statement : global_statement
                  | clear_statement
                  | assignment_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement
        """

    def p_statement_list(self, p: yacc.YaccProduction) -> None:
        """
        statement_list : statement
                       | statement_list statement
        """

    def p_identifier_list(self, p: yacc.YaccProduction) -> None:
        """
        identifier_list : IDENTIFIER
                        | identifier_list IDENTIFIER
        """

    def p_global_statement(self, p: yacc.YaccProduction) -> None:
        """
        global_statement : GLOBAL identifier_list eostmt
        """

    def p_clear_statement(self, p: yacc.YaccProduction) -> None:
        """
        clear_statement : CLEAR identifier_list eostmt
        """

    def p_expression_statement(self, p: yacc.YaccProduction) -> None:
        """
        expression_statement : eostmt
                             | expression eostmt
        """

    def p_assignment_statement(self, p: yacc.YaccProduction) -> None:
        """
        assignment_statement : assignment_expression eostmt
        """

    def p_array_element(self, p: yacc.YaccProduction) -> None:
        """
        array_element : expression
                      | expression_statement
        """

    def p_array_list(self, p: yacc.YaccProduction) -> None:
        """
        array_list : array_element
                   | array_list array_element
        """

    def p_selection_statement(self, p: yacc.YaccProduction) -> None:
        """
        selection_statement : IF expression statement_list END eostmt
                            | IF expression statement_list ELSE statement_list END eostmt
                            | IF expression statement_list elseif_clause END eostmt
                            | IF expression statement_list elseif_clause ELSE statement_list END eostmt
        """

    def p_elseif_clause(self, p: yacc.YaccProduction) -> None:
        """
        elseif_clause : ELSEIF expression statement_list
                      | elseif_clause ELSEIF expression statement_list
        """

    def p_iteration_statement(self, p: yacc.YaccProduction) -> None:
        """
        iteration_statement : WHILE expression statement_list END eostmt
                            | FOR IDENTIFIER '=' expression statement_list END eostmt
                            | FOR '(' IDENTIFIER '=' expression ')' statement_list END eostmt
        """

    def p_jump_statement(self, p: yacc.YaccProduction) -> None:
        """
        jump_statement : BREAK eostmt
                       | RETURN eostmt
        """

    def p_translation_unit(self, p: yacc.YaccProduction) -> None:
        """
        translation_unit : statement_list
                         | FUNCTION func_declare eostmt statement_list
        """

    def p_func_identifier_list(self, p: yacc.YaccProduction) -> None:
        """
        func_identifier_list : IDENTIFIER
                             | func_identifier_list ',' IDENTIFIER
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [*p[1], p[3]]

    def p_func_return_list(self, p: yacc.YaccProduction) -> None:
        """
        func_return_list : IDENTIFIER
                         | '[' func_identifier_list ']'
        """

    def p_func_declare_lhs(self, p: yacc.YaccProduction) -> None:
        """
        func_declare_lhs : IDENTIFIER
                         | IDENTIFIER '(' ')'
                         | IDENTIFIER '(' func_identifier_list ')'
        """

    def p_func_declare(self, p: yacc.YaccProduction) -> None:
        """
        func_declare : func_declare_lhs
                     | func_return_list '=' func_declare_lhs
        """

    def p_error(self, p: yacc.YaccProduction) -> None:
        print(f"Syntax error in input! {p}")


data = '''
if (a == 245)
    do_something
else
    to_do
end



% Just a comment
'''


if __name__ == '__main__':
    parser = Parser(yacc_debug=True)
    ast = parser.parse(text=data, debug_level=False)
