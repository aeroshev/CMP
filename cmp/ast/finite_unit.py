from typing import Any, Dict, Iterator, List

from .node import Node


class SimpleNode(Node):
    """"""
    __slots__ = "content"

    def __init__(self, content: str) -> None:
        self.content = content

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[str]:
        yield self.content

    def __repr__(self) -> str:
        return f'{self.__class__.__name__ }: {self.content}'
