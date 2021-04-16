from .node import Node


class UnaryExpressionNode(Node):
    """"""
    __slots__ = ("unary_op", "expr")

    def __init__(self, unary_op: str, expr: Node) -> None:
        self.unary_op = unary_op
        self.expr = expr
