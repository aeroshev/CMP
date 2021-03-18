from typing import Any, Dict, List

from .node import Node


class IdentifierNode(Node):
    """Identifier object node"""
    __slots__ = "name",

    def __init__(self, name: str) -> None:
        self.name = name

    def children(self) -> List[Dict[str, Any]]:
        return [{"name": self.name}]
