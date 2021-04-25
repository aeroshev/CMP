from typing import Any, List, Union

from ply.yacc import YaccProduction, yacc

from cmp.ast import *
from cmp.grammar import Lexer
from cmp.grammar.cmp_tables import abs_module_path
from cmp.helpers import LogMixin, colors
from cmp.traverse.traverse_ast import Visitor


class Parser(LogMixin):
    """
    Executive parser object.
    Containing primary reduce rules.
    This class build AST
    """
    handlers = {
        "<": LowerRelationalNode,
        ">": GreaterRelationalNode,
        "<=": LowerEqualRelationalNode,
        ">=": GreaterEqualRelationalNode,
        "==": PositiveEqualityNode,
        "!=": NegativeEqualityNode,
        "&": AndNode,
        "|": OrNode,
        "*": MultiplyNode,
        "/": DivideNode,
        "^": PowerNode,
        "+": PlusNode,
        "-": MinusNode,
        ".*": ArrayMulNode,
        ".^": ArrayPowerNode,
        "./": ArrayDivNode,
        ".//": ArrayRDivNode
    }
    _recover_table = frozenset({
        'NEWLINE',
        ';'
    })

    def __init__(
            self,
            lexer=Lexer,
            yacc_debug=True
    ) -> None:
        self._lex = lexer()
        self.tokens = self._lex.tokens
        self.error_messages = []  # type: List[str]
        self._parser = yacc(
            module=self,
            start='translation_unit',
            debug=yacc_debug,
            outputdir=abs_module_path,
            tabmodule='cmp_parse_tab',
            optimize=True,
            errorlog=self.logger
        )

    precedence = (
        ('right', '-'),
        ('right', '~'),
        ('right', '+')
    )

    def _lhs_rhs_expression(self, p: YaccProduction) -> None:
        if len(p) == 4:
            p[0] = self.handlers[p[2]](lhs=p[1], rhs=p[3])
        else:
            p[0] = p[1]

    @staticmethod
    def _save_merge(
            left: Union[List[Node], Node],
            right: Union[List[Node], Node]
    ) -> List[Node]:
        listed_left = [left] if len(left) == 1 else left
        listed_right = [right] if len(right) == 1 else right
        return [*listed_left, *listed_right]

    def parse(self, text, filename='', debug_level=True) -> Any:  # TODO Debug mode
        return self._parser.parsedebug(
            input=text,
            lexer=self._lex,
            debug=self.logger
        )

    def p_primary_expression(self, p: YaccProduction) -> None:
        """
        primary_expression : identifier_expression
                           | constant_expression
                           | string_literal_expression
                           | '(' expression ')'
                           | '[' ']'
                           | '[' array_list ']'
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = ArrayVectorNode(content=[])
        else:
            if p[1] == '[':
                p[0] = ArrayVectorNode(content=p[2])
            elif p[1] == '(':
                p[0] = p[2]

    def p_identifier_expression(self, p: YaccProduction) -> None:
        """
        identifier_expression : IDENTIFIER
        """
        p[0] = IdentifierNode(p[1])

    def p_constant_expression(self, p: YaccProduction) -> None:
        """
        constant_expression : CONSTANT
        """
        p[0] = ConstantNode(p[1])

    def p_string_literal_expression(self, p: YaccProduction) -> None:
        """
        string_literal_expression : STRING_LITERAL
        """
        p[0] = SimpleNode(p[1])

    def p_postfix_expression(self, p: YaccProduction) -> None:
        """
        postfix_expression : primary_expression
                           | array_expression
                           | postfix_expression TRANSPOSE
        """
        p[0] = p[1] if len(p) == 2 else TransposeNode(expr=p[1])

    def p_index_expression(self, p: YaccProduction) -> None:
        """
        index_expression : ':'
                         | expression
        """
        p[0] = p[1] if p[1] != ':' else []  # TODO

    def p_index_expression_list(self, p: YaccProduction) -> None:
        """
        index_expression_list : index_expression
                              | index_expression_list ',' index_expression
        """
        p[0] = p[1] if len(p) == 2 else self._save_merge(left=p[1], right=p[3])

    def p_array_expression(self, p: YaccProduction) -> None:
        """
        array_expression : IDENTIFIER '(' index_expression_list ')'
        """
        p[0] = ArrayNode(ident=p[1], content=p[3])

    def p_unary_expression(self, p: YaccProduction) -> None:
        """
        unary_expression : postfix_expression
                         | unary_operator postfix_expression
        """
        p[0] = p[1] if len(p) == 2 else UnaryExpressionNode(unary_op=p[1], expr=p[2])

    def p_unary_operator(self, p: YaccProduction) -> None:
        """
        unary_operator : '+'
                       | '-'
                       | '~'
        """
        p[0] = p[1]

    def p_multiplicative_expression(self, p: YaccProduction) -> None:
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
        self._lhs_rhs_expression(p)

    def p_additive_expression(self, p: YaccProduction) -> None:
        """
        additive_expression : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative_expression
        """
        self._lhs_rhs_expression(p)

    def p_relational_expression(self, p: YaccProduction) -> None:
        """
        relational_expression : additive_expression
                              | relational_expression '<' additive_expression
                              | relational_expression '>' additive_expression
                              | relational_expression LE_OP additive_expression
                              | relational_expression GE_OP additive_expression
        """
        self._lhs_rhs_expression(p)

    def p_equality_expression(self, p: YaccProduction) -> None:
        """
        equality_expression : relational_expression
                            | equality_expression EQ_OP relational_expression
                            | equality_expression NE_OP relational_expression
        """
        self._lhs_rhs_expression(p)

    def p_and_expression(self, p: YaccProduction) -> None:
        """
        and_expression : equality_expression
                       | and_expression '&' equality_expression
        """
        self._lhs_rhs_expression(p)

    def p_or_expression(self, p: YaccProduction) -> None:
        """
        or_expression : and_expression
                      | or_expression '|' and_expression
        """
        self._lhs_rhs_expression(p)

    def p_expression(self, p: YaccProduction) -> None:
        """
        expression : or_expression
                   | expression ':' or_expression
        """
        p[0] = p[1] if len(p) == 2 else SparseNode(lhs=p[1], rhs=p[3])

    def p_assignment_expression(self, p: YaccProduction) -> None:
        """
        assignment_expression : postfix_expression '=' expression
        """
        p[0] = AssignmentNode(lhs=p[1], rhs=p[3])

    def p_eostmt(self, p: YaccProduction) -> None:
        """
        eostmt : ','
               | ';'
               | NEWLINE
        """
        p[0] = p[1]

    def p_statement(self, p: YaccProduction) -> None:
        """
        statement : global_statement
                  | clear_statement
                  | assignment_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement
                  | func_statement
        """
        p[0] = p[1]

    def p_statement_list(self, p: YaccProduction) -> None:
        """
        statement_list : statement
                       | statement_list statement
                       | statement_list_error
        """
        p[0] = p[1] if len(p) == 2 else self._save_merge(left=p[1], right=p[2])

    def p_statement_list_error(self, p: YaccProduction) -> None:
        """
        statement_list_error : statement_list error
        """
        error_message = (
            f"{colors.WARNING}"
            f"Syntax error at line {p.lineno(1)} in position {p.lexpos(1)}! Handling: {p[2]}"
            f"{colors.ENDC}"
        )
        self.error_messages.append(error_message)
        p[0] = ErrorNode(message=error_message)

    def p_identifier_list(self, p: YaccProduction) -> None:
        """
        identifier_list : IDENTIFIER
                        | identifier_list IDENTIFIER
        """
        p[0] = p[1] if len(p) == 2 else self._save_merge(left=p[1], right=p[2])

    def p_global_statement(self, p: YaccProduction) -> None:
        """
        global_statement : GLOBAL identifier_list eostmt
        """
        p[0] = [GlobalNode(id_list=p[2]), p[3]]

    def p_clear_statement(self, p: YaccProduction) -> None:
        """
        clear_statement : CLEAR identifier_list eostmt
        """
        p[0] = [ClearNode(id_list=p[2]), p[3]]

    def p_expression_statement(self, p: YaccProduction) -> None:
        """
        expression_statement : eostmt
                             | expression eostmt
        """
        p[0] = p[1] if len(p) == 2 else self._save_merge(left=p[1], right=p[2])

    def p_assignment_statement(self, p: YaccProduction) -> None:
        """
        assignment_statement : assignment_expression eostmt
        """
        p[0] = [p[1], p[2]]

    def p_array_element(self, p: YaccProduction) -> None:
        """
        array_element : expression
                      | expression_statement
        """
        p[0] = p[1]

    def p_array_list(self, p: YaccProduction) -> None:
        """
        array_list : array_element
                   | array_list array_element
        """
        p[0] = p[1] if len(p) == 2 else self._save_merge(left=p[1], right=p[2])

    # def p_array_list_error(self, p: YaccProduction) -> None:
    #     """
    #     array_list_error : array_list error
    #     """
    #     p[0] = ErrorNode(message='Syntax error at array element')

    def p_selection_statement(self, p: YaccProduction) -> None:
        """
        selection_statement : IF expression statement_list END eostmt
                            | IF expression statement_list ELSE statement_list END eostmt
                            | IF expression statement_list elseif_clause END eostmt
                            | IF expression statement_list elseif_clause ELSE statement_list END eostmt
                            | selection_statement_invoke_error
        """
        if len(p) == 9:
            p[0] = ManyBranchConditionalNode(main_stmt=p[2], main_branch=p[3], alt_chain=p[4], alt_branch=p[6])
        elif len(p) == 8:
            p[0] = TwoBranchConditionalNode(main_stmt=p[2], main_branch=p[3], alt_branch=p[5])
        elif len(p) == 7:
            p[0] = ManyBranchConditionalNode(main_stmt=p[2], main_branch=p[3], alt_chain=p[4], alt_branch=[])
        elif len(p) == 6:
            p[0] = SimpleConditionalNode(main_stmt=p[2], stmt_list=p[3])

    def p_selection_statement_invoke_error(self, p: YaccProduction) -> None:
        """
        selection_statement_invoke_error : IF expression statement_list
        """
        raise SyntaxError

    def p_elseif_clause(self, p: YaccProduction) -> None:
        """
        elseif_clause : ELSEIF expression statement_list
                      | elseif_clause ELSEIF expression statement_list
        """
        if len(p) == 4:
            p[0] = [ElseIfClauseNode(main_stmt=p[2], stmt_list=p[3])]
        else:
            p[0] = [*p[1], ElseIfClauseNode(main_stmt=p[3], stmt_list=p[4])]

    def p_iteration_statement(self, p: YaccProduction) -> None:
        """
        iteration_statement : WHILE expression statement_list END eostmt
                            | FOR IDENTIFIER '=' expression statement_list END eostmt
                            | FOR '(' IDENTIFIER '=' expression ')' statement_list END eostmt
        """
        if len(p) == 6:
            p[0] = WhileLoopNode(express=p[2], body=p[3])
        else:
            if len(p) == 8:
                p[0] = ForLoopNode(iterator=p[2], express=p[4], body=p[5])
            else:
                p[0] = ForLoopNode(iterator=p[3], express=p[5], body=p[7])

    def p_jump_statement(self, p: YaccProduction) -> None:
        """
        jump_statement : BREAK eostmt
                       | RETURN eostmt
        """
        if p[1] == 'break':
            p[0] = [BreakNode(), p[2]]
        elif p[1] == 'return':
            p[0] = [ReturnNode(), p[2]]

    def p_translation_unit(self, p: YaccProduction) -> None:
        """
        translation_unit : statement_list
        """
        p[0] = FileAST(root=p[1])

    def p_func_identifier_list(self, p: YaccProduction) -> None:
        """
        func_identifier_list : IDENTIFIER
                             | func_identifier_list ',' IDENTIFIER
        """
        if len(p) == 2:
            p[0] = SimpleNode(p[1])
        else:
            p[0] = self._save_merge(left=p[1], right=SimpleNode(p[3]))

    def p_func_return_list(self, p: YaccProduction) -> None:
        """
        func_return_list : IDENTIFIER
                         | '[' func_identifier_list ']'
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_func_declare_lhs(self, p: YaccProduction) -> None:
        """
        func_declare_lhs : IDENTIFIER
                         | IDENTIFIER '(' ')'
                         | IDENTIFIER '(' func_identifier_list ')'
        """
        if len(p) < 5:
            p[0] = FunctionNameNode(name=p[1], input_list=[])
        else:
            p[0] = FunctionNameNode(name=p[1], input_list=p[3])

    def p_func_declare(self, p: YaccProduction) -> None:
        """
        func_declare : func_declare_lhs
                     | func_return_list '=' func_declare_lhs
        """
        if len(p) == 2:
            p[0] = FunctionDeclareNode(return_list=[], name=p[1])
        else:
            p[0] = FunctionDeclareNode(return_list=p[1], name=p[3])

    def p_func_statement(self, p: YaccProduction) -> None:
        """
        func_statement : FUNCTION func_declare eostmt statement_list END
        """
        p[0] = FunctionNode(declare=p[2], body=p[4])

    def p_error(self, p: YaccProduction) -> None:
        # Panic recovery mode
        line = p.lineno if p else ''
        index = p.lexpos if p else ''
        name_tok = p.type if p else p
        self.error_messages.append(
            f"{colors.WARNING}"
            f"Syntax error at line {line} in position {index}! Handling: {name_tok}"
            f"{colors.ENDC}"
        )
        while True:
            token = self._parser.token()
            if not token or token.type in self._recover_table:
                break
        self._parser.restart()


# TODO Debug mode
data = '''
a = [1; 2);

b = [1; 2; 3]

if (a == 2)
    s = 1

c = 4

'''


if __name__ == '__main__':
    parser = Parser(yacc_debug=True)
    ast = parser.parse(text=data, debug_level=False)
    if len(parser.error_messages) > 0:
        for message in parser.error_messages:
            print(message)
    else:
        v = Visitor()
        res = v.traverse_ast(ast)
        print(res)
