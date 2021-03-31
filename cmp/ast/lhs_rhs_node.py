from typing import Any, Dict, Iterator, List
from itertools import chain


from .node import Node


class LhsRhsNode(Node):
    """Base for lhs, rhs object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def children(self) -> List[Any]:
        nodes_list = []
        nodes_list.append(self.__class__.__name__)
        if self.lhs is not None:
            nodes_list += self.lhs.children()
        if self.rhs is not None:
            nodes_list += self.rhs.children()
        return nodes_list

    def __iter__(self) -> Iterator[Node]:
        yield self
        # if self.lhs:
        #     yield self.lhs
        # if self.rhs:
        #     yield self.rhs

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: lhs({self.lhs}) rhs({self.rhs})'
