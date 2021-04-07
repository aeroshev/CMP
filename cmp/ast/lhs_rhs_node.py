from .node import Node


class LhsRhsNode(Node):
    """Base for lhs, rhs object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: lhs({self.lhs}) rhs({self.rhs})'
