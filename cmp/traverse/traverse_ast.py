from typing import Any, List, Optional, TextIO

from cmp.ast import *
from cmp.helpers import camel_to_snake


class Visitor:
    """
    Walk through the generated AST and
    translating it to Python code in the specified file
    """
    def __init__(self, filename: str = 'output.py') -> None:
        self.depth = 0  # type: int
        self._output = open(filename, "w", encoding="utf-8")  # type: TextIO

    def __del__(self) -> None:
        self._output.close()

    @property
    def python_tabulate(self) -> str:
        return ' ' * 4 * self.depth

    def traverse_ast(self, root: FileAST, use_file: bool = False) -> Optional[str]:
        res_str = ''
        for node in root:
            res_str += self._visit(node)
        if use_file:
            self._output.write(res_str)
            return None
        else:
            return res_str

    def _visit(self, node: Node) -> Any:
        method = '_visit_' + camel_to_snake(node.__class__.__name__)
        self.depth += 1
        res = getattr(self, method)(node)
        self.depth -= 1
        return res

    def _visit_list(self, list_nodes: List[Node]) -> List[str]:
        res = []
        for node in list_nodes:
            res.append(self._visit(node))
        return res

    def _visit_two_branch_conditional_node(
            self,
            node: TwoBranchConditionalNode
    ) -> str:
        main_stmt = self._visit(node.main_stmt)
        main_branch = ''
        for elem in self._visit_list(node.main_branch):
            main_branch += f'{self.python_tabulate}{elem}'
        alt_branch = ''
        for elem in self._visit_list(node.alt_branch):
            alt_branch += f'{self.python_tabulate}{elem}'
        output_str = (
            f'if {main_stmt}:\n'
            f'{main_branch}'
            f'else:\n'
            f'{alt_branch}'
        )
        return output_str

    def _visit_assignment_node(self, node: AssignmentNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'{lhs} = {rhs}\n'   # ???

    def _visit_simple_node(self, node: SimpleNode) -> str:
        return node.content

    def _visit_array_vector_node(self, node: ArrayVectorNode) -> str:
        res = []
        for elem in node.content:
            res.append(self._visit(elem))
        return '[' + ', '.join(res) + ']'

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
        body = self._visit_list(node.body)
        body_str = ''
        for instruction in body:
            body_str += f'{self.python_tabulate}{instruction}'
        return f'for {iterator} in {expression}:\n' + body_str

    def _visit_sparse_node(self, node: SparseNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        return f'range({lhs}, {rhs})'

    def _visit_simple_conditional_node(self, node: SimpleConditionalNode) -> str:
        main_stmt = self._visit(node.main_stmt)
        main_branch = ''
        for elem in self._visit_list(node.stmt_list):
            main_branch += f'{self.python_tabulate}{elem}'
        output_str = (
            f'if {main_stmt}:\n'
            f'{main_branch}'
        )
        return output_str

    def _visit_break_node(self, node: BreakNode) -> str:
        return 'break\n'
