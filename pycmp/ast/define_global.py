from typing import List

from .node import Node


class GlobalNode(Node):
    """Object of global key word"""
    __slots__ = "id_list"

    def __init__(self, id_list: List[Node]) -> None:
        self.id_list = id_list
