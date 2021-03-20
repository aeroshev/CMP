from typing import Any, Dict, List

from .node import Node


class GlobalNode(Node):
    """"""
    __slots__ = "id_list"

    def __init__(self, id_list: List[Node]) -> None:
        self.id_list = id_list

    def children(self) -> List[Dict[str, Any]]:
        ...
