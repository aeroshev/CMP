from typing import Any, Iterator, List

from .node import Node


class FileAST(Node):
    """"""
    __slots__ = "root"

    def __init__(self, root: Node) -> None:
        self.root = root

    def __iter__(self) -> Iterator[Node]:
        for stmt in self.root:
            yield stmt

    def children(self) -> List[Any]:
        nodes_list = []
        for elem in self.root:
            nodes_list += elem.children()
        return nodes_list
