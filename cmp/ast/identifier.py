from .node import Node


class IdentifierNode(Node):
    """"""
    __slots__ = "name",

    def __init__(self, name: str) -> None:
        self.name = name

    def children(self):
        ...
