from .node import Node


class IdentifierNode(Node):
    """Identifier object node"""
    __slots__ = "name",

    def __init__(self, name: str) -> None:
        self.name = name
