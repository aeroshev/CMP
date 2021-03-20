from .lhs_rhs_node import LhsRhsNode
from .node import Node


class AndNode(LhsRhsNode):
    """"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class OrNode(LhsRhsNode):
    """"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
