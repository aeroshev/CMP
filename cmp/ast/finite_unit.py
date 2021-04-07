from .node import Node


class SimpleNode(Node):
    """Finite point in traverse tree"""
    __slots__ = "content"

    def __init__(self, content: str) -> None:
        self.content = content

    def __repr__(self) -> str:
        return f'{self.__class__.__name__ } ({self.content})'
