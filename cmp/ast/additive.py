from .node import Node
from .lhs_rhs_node import LhsRhsNode


class PlusNode(LhsRhsNode):
    """"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class MinusNode(LhsRhsNode):
    """"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
