from .node import Node
from .lhs_rhs_node import LhsRhsNode


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
