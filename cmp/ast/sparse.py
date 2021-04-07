from .lhs_rhs_node import LhsRhsNode
from .node import Node


class SparseNode(LhsRhsNode):
    """Smudge value"""
    __slots__ = ("lhs", 'rhs')

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
