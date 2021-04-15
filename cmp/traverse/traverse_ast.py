from typing import Any, Iterator, List, Optional, TextIO, Tuple, Union

from cmp.ast import *
from cmp.helpers import BadInputError, camel_to_snake


class Visitor:
    """
    Walk through the generated AST and
    translating it to Python code in the specified file
    """
    def __init__(self, filename: str = None) -> None:
        self.depth = 0  # type: int
        if filename:
            self._output = open(filename, "w", encoding="utf-8")  # type: TextIO

    def __del__(self) -> None:
        if hasattr(self, '_output'):
            self._output.close()

    @property
    def python_tabulate(self) -> str:
        return ' ' * 4 * self.depth

    def traverse_ast(self, root: FileAST) -> Optional[str]:
        if root is None:
            raise BadInputError('Root of AST is None')

        res_str = 'import numpy as np' + '\n\n'
        for node in root:
            res_str += self._visit(node)

        if hasattr(self, '_output'):
            self._output.write(res_str)
            return None
        else:
            return res_str

    def _visit(self, node: Union[Node, List[Node], List[str]]) -> Any:
        method = '_visit_' + camel_to_snake(node.__class__.__name__)
        self.depth += 1
        res = getattr(self, method)(node)
        self.depth -= 1
        return res

    def _visit_list(self, list_nodes: List[Node]) -> List[str]:
        self.depth -= 1
        res = []
        for node in list_nodes:
            res.append(self._visit(node))
        self.depth += 1
        return res

    def _visit_two_branch_conditional_node(
            self,
            node: TwoBranchConditionalNode
    ) -> str:
        main_stmt = self._visit(node.main_stmt)
        main_branch = ''
        for elem in self._visit(node.main_branch):
            main_branch += f'{self.python_tabulate}{elem}'
        alt_branch = ''
        for elem in self._visit(node.alt_branch):
            alt_branch += f'{self.python_tabulate}{elem}'
        output_str = (
            f'if {main_stmt}:'
            f'{main_branch}'
            f'else:'
            f'{alt_branch}'
        )
        return output_str

    def _visit_assignment_node(self, node: AssignmentNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} = {rhs}'

    def _visit_simple_node(self, node: SimpleNode) -> str:
        return node.content

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

    def _visit_array_vector_node(self, node: ArrayVectorNode) -> str:
        res = ''
        list_elems = []
        res += '['
        for shape, chunk in enumerate(self._split_by_chunks(node.content)):
            for elem in chunk:
                list_elems.append(self._visit(elem))
            res += '[' + ', '.join(list_elems) + ']'
            list_elems = []
        res += ']'

        return f'np.array({res})'

    def _visit_multiply_node(self, node: MultiplyNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} * {rhs}'

    def _visit_positive_equality_node(self, node: PositiveEqualityNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} == {rhs}'

    def _visit_for_loop_node(self, node: ForLoopNode) -> str:
        iterator = node.iter
        expression = self._visit(node.express)
        body = self._visit(node.body)
        body_str = ''
        for instruction in body:
            body_str += f'{self.python_tabulate}{instruction}'
        return f'for {iterator} in {expression}:' + body_str

    def _visit_sparse_node(self, node: SparseNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'range({lhs}, {rhs})'

    def _visit_simple_conditional_node(self, node: SimpleConditionalNode) -> str:
        main_stmt = self._visit(node.main_stmt)
        main_branch = ''
        for elem in self._visit(node.stmt_list):
            main_branch += f'{self.python_tabulate}{elem}'
        output_str = (
            f'if {main_stmt}:'
            f'{main_branch}'
        )
        return output_str

    def _visit_break_node(self, node: BreakNode) -> str:
        return 'break'

    def _visit_function_node(self, node: FunctionNode) -> str:
        declare, return_list = self._visit(node.declare)
        body = self._visit(node.body)
        body_str = ''
        for instruction in body:
            body_str += f'{self.python_tabulate}{instruction}'
        return_str = f'{self.python_tabulate}return '
        return_str += ', '.join(return_list)
        func_str = f'def {declare}:\n' + body_str + return_str
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

    @staticmethod
    def _visit_str(string: str) -> str:
        if string == ';':
            return ''
        return string

    def _visit_plus_node(self, node: PlusNode) -> str:  # TODO add pattern
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} + {rhs}'

    def _visit_unary_expression_node(self, node: UnaryExpressionNode) -> str:
        return f'{node.unary_op}{self._visit(node.expr)}'

    def _visit_identifier_node(self, node: IdentifierNode) -> str:
        return node.ident

    def _visit_constant_node(self, node: ConstantNode) -> str:
        return node.const
