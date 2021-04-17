from .node import Node


class UnaryExpressionNode(Node):
    """Node of unary operator"""
    __slots__ = ("unary_op", "expr")

    def __init__(self, unary_op: str, expr: Node) -> None:
        self.unary_op = unary_op
        self.expr = expr
