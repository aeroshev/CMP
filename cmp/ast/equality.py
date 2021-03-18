from typing import Any, Dict, List

from .node import Node


class EqualityNode(Node):
    """Equality object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def children(self) -> List[Dict[str, Any]]:
        node_list = []
        if self.lhs is not None:
            node_list.append({"lhs": self.lhs})
        if self.rhs is not None:
            node_list.append({"rhs": self.rhs})
        return node_list


class PositiveEqualityNode(EqualityNode):
    """Positive equality object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)


class NegativeEqualityNode(EqualityNode):
    """Negative equality object node"""
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs: Node, rhs: Node) -> None:
        super().__init__(lhs, rhs)
