from typing import List

from .node import Node


class ForLoopNode(Node):
    """Object of FOR loop"""
    __slots__ = ('iter', 'express', 'body')

    def __init__(self, iterator: Node, express: Node, body: List[Node]) -> None:
        self.iter = iterator
        self.express = express
        self.body = body
