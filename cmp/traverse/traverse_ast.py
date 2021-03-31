from typing import Any

from cmp.ast import *
from cmp.helpers import camel_to_snake


class Visitor:
    """"""
    def __init__(self, filename: str) -> None:
        self._output = open(filename, "w", encoding="utf-8")

    def __del__(self) -> None:
        self._output.close()

    def visit(self, node: Node) -> Any:
        method = 'visit_' + camel_to_snake(node.__class__.__name__)
        return getattr(self, method)(node)

    def visit_two_branch_conditional_node(
            self,
            node: TwoBranchConditionalNode
    ) -> None:
        output_str = (
            f'if {node.main_stmt}:\n'
            f'\t{node.main_branch}\n'
            f'else:\n'
            f'\t{node.alt_branch}'
        )
        self._output.write(output_str)

    def visit_assignment_node(self, node: AssignmentNode) -> None:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        print(f'lhs {lhs}, rhs {rhs}')
        self._output.write(f'{lhs} = {rhs}')

    def visit_simple_node(self, node: SimpleNode) -> str:
        print(node.content)
        return node.content

    def visit_array_vector_node(self, node: ArrayVectorNode) -> str:
        res = []
        for elem in node.content:
            res.append(self.visit(elem))
        return '[' + ', '.join(res) + ']'

    def visit_multiply_node(self, node: MultiplyNode) -> str:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f'{lhs} * {rhs}'
