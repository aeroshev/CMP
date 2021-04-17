from .node import Node


class TransposeNode(Node):
    """Node of transpose operation"""
    __slots__ = "expr"

    def __init__(self, expr: Node) -> None:
        self.expr = expr
