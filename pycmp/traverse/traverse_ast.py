from typing import Any, Iterator, List, Optional, TextIO, Tuple, Union

from pycmp.ast import *
from pycmp.helpers import BadInputError, camel_to_snake, colors


class Visitor:
    """
    Walk through the generated AST and
    translating it to Python code in the specified file
    Recursive walking in tree invoke methods _visit + NameNode
    numpy_mode - if activated, ordinary operation will be translated
        in numpy operations
    filename - name of file where will be written python code
    _depth - inner variable for count indent
    _stack - store for return value of function
    """
    keywords = {
        'zeros': 'np.zeros',
        'ones': 'np.ones',
        'rand': 'np.random',
        'eye': 'np.eye',
        'diag': 'np.diag'
    }

    def __init__(self, numpy_mode: bool = False, filename: str = None) -> None:
        self._depth = 0  # type: int
        self._stack = []  # type: List[Any]
        self.numpy_mode = numpy_mode
        if filename:
            self._output = open(filename, "w", encoding="utf-8")  # type: TextIO

    def __del__(self) -> None:
        if hasattr(self, '_output'):
            self._output.close()

    def traverse_ast(self, root: FileAST) -> Optional[str]:
        """
        Main function for traverse and printing translated code.
        :param: root: FileAST - root of AST
        :return: python code or None if a file
        was specified when creating an object
        """
        if root is None:
            raise BadInputError('Root of AST is None')

        res_str = 'import numpy as np' + '\n\n\n'
        for node in root:
            res_str += self._visit(node)

        if hasattr(self, '_output'):
            self._output.write(res_str)
            return None
        else:
            return res_str

    def _visit(self, node: Union[Node, List[Node], List[str]]) -> Any:
        method = '_visit_' + camel_to_snake(node.__class__.__name__)
        self._depth += 1
        res = getattr(self, method)(node)
        self._depth -= 1
        return res

    @property
    def py_tab(self) -> str:
        return ' ' * 4 * self._depth

    def tabulate_expr(self, expr: str) -> str:
        """
        Shift expression on python tab
        and filtering entered expression
        on empty symbol or \n symbol
        """
        if expr == '\n':
            return expr
        if len(expr) > 0:
            return f'{self.py_tab}{expr}'
        return ''

    @staticmethod
    def _split_by_chunks(big_list: List[Node]) -> Iterator[List[Node]]:
        chunk = []  # type: List[Node]
        for elem in big_list:
            if elem == ';':
                yield chunk
                chunk = []
                continue
            if elem == ',':
                continue
            chunk.append(elem)
        yield chunk

    # Built-in Python types
    @staticmethod
    def _visit_str(string: str) -> str:
        if string == ';':
            return ''
        return string

    def _visit_list(self, list_nodes: List[Node]) -> List[str]:
        self._depth -= 1
        res = []
        for node in list_nodes:
            res.append(self._visit(node))
        self._depth += 1
        return res

    # Additive group
    def _visit_plus_node(self, node: PlusNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        if self.numpy_mode:
            return f'np.add({lhs}, {rhs})'
        return f'{lhs} + {rhs}'

    def _visit_minus_node(self, node: MinusNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        if self.numpy_mode:
            return f'np.subtract({lhs}, {rhs})'
        return f'{lhs} - {rhs}'

    # Array group
    def _visit_array_vector_node(self, node: ArrayVectorNode) -> str:
        list_elems = []  # type: List[List[str]]
        for shape, chunk in enumerate(self._split_by_chunks(node.content)):
            list_elems.append([])
            for elem in chunk:
                list_elems[shape].append(self._visit(elem))

        res = ''
        rows_str_list = []
        for row in list_elems:
            rows_str_list.append('[' + ', '.join(row) + ']')
        res += '[' + ', '.join(rows_str_list) + ']'

        return f'np.array({res})'

    def _visit_array_node(self, node: ArrayNode) -> str:
        name = self._visit(node.ident)
        name_str = (name, self.keywords[name])[name in list(self.keywords)]
        index_list = [i_expr for i_expr in self._visit(node.content)]
        index_str = ', '.join(index_list)
        return f'{name_str}({index_str})'

    # Assignment group
    def _visit_assignment_node(self, node: AssignmentNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} = {rhs}'

    # Comment group
    def _visit_comment_node(self, node: CommentNode) -> str:
        return f'#{node.comment}'

    # Conditional statement group
    def _visit_simple_conditional_node(self, node: SimpleConditionalNode) -> str:
        main_stmt = self._visit(node.main_stmt)

        main_branch = ''
        for elem in self._visit(node.stmt_list):
            main_branch += self.tabulate_expr(elem)

        output_str = (
            f'if {main_stmt}:'
            f'{main_branch}'
        )
        return output_str

    def _visit_two_branch_conditional_node(
            self,
            node: TwoBranchConditionalNode
    ) -> str:
        main_stmt = self._visit(node.main_stmt)

        main_branch = ''
        for elem in self._visit(node.main_branch):
            main_branch += self.tabulate_expr(elem)

        alt_branch = ''
        for elem in self._visit(node.alt_branch):
            alt_branch += self.tabulate_expr(elem)

        self._depth -= 1
        output_str = (
            f'if {main_stmt}:'
            f'{main_branch}'
            f'{self.py_tab}else:'
            f'{alt_branch}'
        )
        self._depth += 1
        return output_str

    def _visit_else_if_clause_node(self, node: ElseIfClauseNode) -> str:
        main_stmt = self._visit(node.main_stmt)

        main_branch = ''
        for elem in self._visit(node.stmt_list):
            main_branch += self.tabulate_expr(elem)

        output_str = (
            f'elif {main_stmt}:'
            f'{main_branch}'
        )
        return output_str

    def _visit_many_branch_conditional_node(self, node: ManyBranchConditionalNode) -> str:
        main_stmt = self._visit(node.main_stmt)

        main_branch = ''
        for elem in self._visit(node.main_branch):
            main_branch += self.tabulate_expr(elem)

        self._depth -= 1
        alt_chain = ''
        for cond in self._visit(node.alt_chain):
            alt_chain += self.tabulate_expr(cond)
        self._depth += 1

        alt_branch = ''
        for elem in self._visit(node.alt_branch):
            alt_branch += self.tabulate_expr(elem)

        output_str = (
            f'if {main_stmt}:'
            f'{main_branch}'
            f'{alt_chain}'
        )
        if len(alt_branch) > 0:
            self._depth -= 1
            output_str += (
                f'{self.py_tab}else:'
                f'{alt_branch}'
            )
            self._depth += 1
        return output_str

    # Define clear group
    def _visit_clear_node(self, node: ClearNode) -> str:
        id_list = self._visit(node.id_list)
        res_str = ''
        for var in id_list:
            res_str += f'{var} = None\n'
        return res_str

    # Define global group
    def _visit_global_node(self, node: GlobalNode) -> str:
        id_list = self._visit(node.id_list)
        res_str = 'global ' + ', '.join(id_list)
        return res_str

    # Equality group
    def _visit_positive_equality_node(self, node: PositiveEqualityNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} == {rhs}'

    def _visit_negative_equality_node(self, node: NegativeEqualityNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} != {rhs}'

    # Error group
    def _visit_error_node(self, node: ErrorNode) -> str:
        return f'{colors.WARNING}!{node.message}!{colors.ENDC}'

    # Finite unit group
    @staticmethod
    def _visit_simple_node(node: SimpleNode) -> str:
        return node.content

    @staticmethod
    def _visit_identifier_node(node: IdentifierNode) -> str:
        return node.ident

    @staticmethod
    def _visit_constant_node(node: ConstantNode) -> str:
        return node.const

    # Function group
    def _visit_function_node(self, node: FunctionNode) -> str:
        declare, return_list = self._visit(node.declare)
        self._stack.append(return_list)
        body = self._visit(node.body)

        body_str = ''
        for instruction in body:
            body_str += self.tabulate_expr(instruction)
        return_str = self.tabulate_expr('return ')
        return_str += ', '.join(return_list)
        func_str = f'def {declare}:\n' + body_str + return_str

        self._stack.pop()
        return func_str

    def _visit_function_declare_node(self, node: FunctionDeclareNode) -> Tuple[str, Optional[List[str]]]:
        name = self._visit(node.name)
        return_list = self._visit(node.return_list)
        return_list_str = []
        for elem in return_list:
            return_list_str.append(elem)
        return f'{name}', return_list_str

    def _visit_function_name_node(self, node: FunctionNameNode) -> str:
        name = self._visit(node.name)
        input_list = self._visit(node.input_list)
        input_str = ', '.join(input_list)
        return f'{name}({input_str})'

    # Iteration group
    def _visit_for_loop_node(self, node: ForLoopNode) -> str:
        iterator = node.iter
        expression = self._visit(node.express)
        body = self._visit(node.body)
        body_str = ''
        for instruction in body:
            body_str += self.tabulate_expr(instruction)
        return f'for {iterator} in {expression}:' + body_str

    def _visit_while_loop_node(self, node: WhileLoopNode) -> str:
        expression = self._visit(node.express)
        body = self._visit(node.body)
        body_str = ''
        for instruction in body:
            body_str += self.tabulate_expr(instruction)
        return f'while {expression}:' + body_str

    # Jump statement group
    @staticmethod
    def _visit_break_node(node: BreakNode) -> str:
        return 'break'

    def _visit_return_node(self, node: ReturnNode) -> str:
        if len(self._stack) > 0:
            return_list = self._stack[-1]
            return_str = 'return ' + ', '.join(return_list)
            return return_str
        return self.tabulate_expr('return')

    # Logic group
    def _visit_and_node(self, node: AndNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} and {rhs}'

    def _visit_or_node(self, node: OrNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} or {rhs}'

    # Multiplicative group
    def _visit_multiply_node(self, node: MultiplyNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} * {rhs}'

    def _visit_divide_node(self, node: DivideNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} / {rhs}'

    def _visit_power_node(self, node: PowerNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} ** {rhs}'

    def _visit_array_mul_node(self, node: ArrayMulNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'np.multiply({lhs}, {rhs})'

    def _visit_array_div_node(self, node: ArrayDivNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'np.divide({lhs}, {rhs})'

    def _visit_array_r_div_node(self, node: ArrayRDivNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'np.divide({rhs}, {lhs})'

    def _visit_array_power_node(self, node: ArrayPowerNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'np.power({lhs}, {rhs})'

    # Relational group
    def _visit_greater_relational_node(self, node: GreaterRelationalNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} > {rhs}'

    def _visit_greater_equal_relational_node(self, node: GreaterEqualRelationalNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} >= {rhs}'

    def _visit_lower_relational_node(self, node: LowerRelationalNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} < {rhs}'

    def _visit_lower_equal_relational_node(self, node: LowerEqualRelationalNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} <= {rhs}'

    # Sparse group
    def _visit_sparse_node(self, node: SparseNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'range({lhs}, {rhs})'

    # Transpose group
    def _visit_transpose_node(self, node: TransposeNode) -> str:
        expr = self._visit(node.expr)
        return f'np.transpose({expr})'

    # Unary expression group
    def _visit_unary_expression_node(self, node: UnaryExpressionNode) -> str:
        return f'{node.unary_op}{self._visit(node.expr)}'
