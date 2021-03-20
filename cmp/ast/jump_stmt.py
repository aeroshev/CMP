from typing import Any, Dict, List

from .node import Node


class BreakNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...


class ReturnNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...
