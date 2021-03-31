from typing import Iterator, List, Any

from .node import Node

class FileAST(Node):
    """"""
    __slots__ = "root"

    def __init__(self, root: Node) -> None:
        self.root = root

    def __iter__(self) -> Iterator[Node]:
        yield self.root

    def children(self) -> List[Any]:
        nodes_list = []
        for elem in self.root:
            nodes_list += elem.children()
        return nodes_list
