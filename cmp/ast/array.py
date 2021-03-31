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


class ArrayVectorNode(Node):
    """"""
    __slots__ = "content"

    def __init__(self, content: List[Node]) -> None:
        self.content = content

    def children(self) -> List[Any]:
        nodes_list = []
        nodes_list.append(self.__class__.__name__)
        for elem in self.content:
            nodes_list += elem.children()
        return nodes_list

    def __iter__(self) -> Iterator[Node]:
        yield self
        # for index in chain(self.content):
        #     yield index
