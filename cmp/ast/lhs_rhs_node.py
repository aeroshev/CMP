from typing import Any, Dict, Iterator, List

from .node import Node


class LhsRhsNode(Node):
    """Base for lhs, rhs object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def children(self) -> List[Dict[str, Any]]:
        nodes_list = []
        if self.lhs is not None:
            nodes_list.append({"lhs": self.lhs})
        if self.rhs is not None:
            nodes_list.append({"rhs": self.rhs})
        return nodes_list

    def __iter__(self) -> Iterator[Node]:
        yield self
        if self.lhs:
            yield self.lhs
        if self.rhs:
            yield self.rhs

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: lhs - {self.lhs}, rhs - {self.rhs}'
