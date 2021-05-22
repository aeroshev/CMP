from .node import Node


class SimpleNode(Node):
    """Finite point in traverse tree"""
    __slots__ = "content"

    def __init__(self, content: str) -> None:
        self.content = content

    def __repr__(self) -> str:
        return f'{self.__class__.__name__ } ({self.content})'


class IdentifierNode(Node):
    """Node of identifier"""
    __slots__ = "ident"

    def __init__(self, ident: str) -> None:
        self.ident = ident


class ConstantNode(Node):
    """Node of constant"""
    __slots__ = "const"

    def __init__(self, const: str) -> None:
        self.const = const
