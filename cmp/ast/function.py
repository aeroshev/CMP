from typing import List

from .node import Node


class FunctionNode(Node):
    """Node of function object"""
    __slots__ = ("declare", "body")

    def __init__(self, declare: Node, body: List[Node]) -> None:
        self.declare = declare
        self.body = body


class FunctionDeclare(Node):
    """Declaration of function"""

    __slots__ = ("return_list", "name")

    def __init__(self, return_list: Node, name: Node) -> None:
        self.return_list = return_list
        self.name = name
