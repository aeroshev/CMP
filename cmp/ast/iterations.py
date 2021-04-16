from typing import List

from .node import Node


class ForLoopNode(Node):
    """Object of FOR loop"""
    __slots__ = ("iter", "express", "body")

    def __init__(self, iterator: Node, express: Node, body: List[Node]) -> None:
        self.iter = iterator
        self.express = express
        self.body = body


class WhileLoopNode(Node):
    """"""
    __slots__ = ("express", "body")

    def __init__(self, express: Node, body: List[Node]) -> None:
        self.express = express
        self.body = body
