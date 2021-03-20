from .lhs_rhs_node import LhsRhsNode
from .node import Node


class GreaterRelationalNode(LhsRhsNode):
    """Greater relational object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class GreaterEqualRelationalNode(LhsRhsNode):
    """Greater or equal relational object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class LowerRelationalNode(LhsRhsNode):
    """Lower object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class LowerEqualRelationalNode(LhsRhsNode):
    """Lower or equal object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
