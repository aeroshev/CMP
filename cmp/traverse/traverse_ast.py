from typing import Any, List, Optional

from cmp.ast import *
from cmp.helpers import camel_to_snake


class Visitor:
    """
    Walk through the generated AST and
    translating it to Python code in the specified file
    """
    def __init__(self, filename: str = '/Users/artem/MyProjects/CMP/tests/output.py') -> None:
        self._output = open(filename, "w", encoding="utf-8")

    def __del__(self) -> None:
        self._output.close()

    @property
    def python_tabulate(self) -> str:
        return ' ' * 4

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
        return getattr(self, method)(node)

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
        main_branch = '\n'.join(self._visit_list(node.main_branch))
        alt_branch = '\n'.join(self._visit_list(node.alt_branch))
        output_str = (
            f'if {main_stmt}:\n'
            f'{self.python_tabulate}{main_branch}\n'
            f'else:\n'
            f'{self.python_tabulate}{alt_branch}'
        )
        return str(output_str)

    def _visit_assignment_node(self, node: AssignmentNode) -> str:
        lhs = self._visit(node.lhs)
        rhs = self._visit(node.rhs)
        print(f'lhs {lhs}, rhs {rhs}')
        return f'{lhs} = {rhs}'

    def _visit_simple_node(self, node: SimpleNode) -> str:
        print(node.content)
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
