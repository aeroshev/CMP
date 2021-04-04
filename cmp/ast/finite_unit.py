from typing import Any, Iterator, List

from .node import Node


class SimpleNode(Node):
    """"""
    __slots__ = "content"

    def __init__(self, content: str) -> None:
        self.content = content

    def children(self) -> List[Any]:
        return []

    def __iter__(self) -> Iterator[Node]:
        yield self

    def __repr__(self) -> str:
        return f'{self.__class__.__name__ } ({self.content})'
