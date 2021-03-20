from cmp.ast import *


class Visitor:
    """"""
    def __init__(self, filename: str) -> None:
        self._output = open(filename, "w", encoding="utf-8")

    def __del__(self) -> None:
        self._output.close()

    def visit(self, node: Node) -> None:
        method = 'visit_' + node.__class__.__name__  # TODO Convert Camel case to Snake case
        getattr(self, method)(node)

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
