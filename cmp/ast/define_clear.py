from typing import Any, Dict, Iterator, List

from .node import Node


class ClearNode(Node):
    """"""
    __slots__ = "id_list"

    def __init__(self, id_list: List[Node]) -> None:
        self.id_list = id_list

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[Node]:
        for _id in self.id_list:
            yield _id
