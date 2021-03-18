from .node import Node
from .lhs_rhs_node import LhsRhsNode


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