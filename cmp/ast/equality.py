from .lhs_rhs_node import LhsRhsNode
from .node import Node


class PositiveEqualityNode(LhsRhsNode):
    """Positive equality object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class NegativeEqualityNode(LhsRhsNode):
    """Negative equality object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
