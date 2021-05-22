from typing import List

from .node import Node


class ArrayNode(Node):
    """
    Create array by defined rules
    Expected expression like
    >>> zeros(1, 5)
    and etc
    """
    __slots__ = ("ident", "content")

    def __init__(self, ident: Node, content: List[Node]) -> None:
        self.ident = ident
        self.content = content


class ArrayVectorNode(Node):
    """
    Node of vector array
    Expected expression like
    >>> [1, 2, 3, 4 * 3]
    and etc
    """
    __slots__ = "content"

    def __init__(self, content: List[Node]) -> None:
        self.content = content
