from typing import Any, Dict, Iterator, List

from .node import Node


class ArrayNode(Node):
    """"""
    __slots__ = ("ident", "content")

    def __init__(self, ident: Node, content: List[Node]) -> None:
        self.ident = ident
        self.content = content

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[Node]:
        yield self.ident
        for index in self.content:
            yield index
