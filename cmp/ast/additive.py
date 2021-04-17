from .lhs_rhs_node import LhsRhsNode
from .node import Node


class PlusNode(LhsRhsNode):
    """Node of plus operation"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class MinusNode(LhsRhsNode):
    """Node of minus operation"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
