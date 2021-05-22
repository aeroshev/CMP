from .lhs_rhs_node import LhsRhsNode
from .node import Node


class MultiplyNode(LhsRhsNode):
    """Object of multiply"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class DivideNode(LhsRhsNode):
    """Object of divide"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class PowerNode(LhsRhsNode):
    """Object of power"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class ArrayMulNode(LhsRhsNode):
    """Object of multiply array"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class ArrayDivNode(LhsRhsNode):
    """Object of divide array"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class ArrayRDivNode(LhsRhsNode):
    """Object of right divide array"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class ArrayPowerNode(LhsRhsNode):
    """Object of power array"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
