from typing import Any, List

from cmp.ast import *
from cmp.helpers import camel_to_snake, defer_string


class Visitor:
    """"""
    def __init__(self, filename: str) -> None:
        self._output = open(filename, "w", encoding="utf-8")

    def __del__(self) -> None:
        self._output.close()

    def visit(self, node: Node) -> Any:
        method = 'visit_' + camel_to_snake(node.__class__.__name__)
        return getattr(self, method)(node)

    def visit_list(self, list_nodes: List[Node]) -> List[Any]:
        res = []
        for node in list_nodes:
            res.append(self.visit(node))
        return res

    def visit_two_branch_conditional_node(
            self,
            node: TwoBranchConditionalNode
    ) -> None:
        output_str = defer_string(
            'if {main_stmt}:\n'
            '\t{main_branch}\n'
            'else:\n'
            '\t{alt_branch}'
        )
        main_stmt = self.visit(node.main_stmt)
        main_branch = '\n'.join(self.visit_list(node.main_branch))
        alt_branch = '\n'.join(self.visit_list(node.alt_branch))
        return str(output_str)

    def visit_assignment_node(self, node: AssignmentNode) -> None:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        print(f'lhs {lhs}, rhs {rhs}')
        return f'{lhs} = {rhs}'

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

    def visit_positive_equality_node(self, node: PositiveEqualityNode) -> str:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f'{lhs} == {rhs}'
