from typing import List, Optional

from .node import Node


class FunctionNode(Node):
    """Node of function object"""
    __slots__ = ("declare", "body")

    def __init__(self, declare: Node, body: List[Node]) -> None:
        self.declare = declare
        self.body = body


class FunctionDeclareNode(Node):
    """Declaration of function"""
    __slots__ = ("return_list", "name")

    def __init__(self, return_list: Optional[Node], name: Node) -> None:
        self.return_list = return_list
        self.name = name


class FunctionNameNode(Node):
    """"""
    __slots__ = ("name", "input_list")

    def __init__(self, name: Node, input_list: Optional[List[Node]]) -> None:
        self.name = name
        self.input_list = input_list
