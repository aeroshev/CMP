from typing import Any, Dict, List

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
