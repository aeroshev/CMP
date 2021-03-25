from typing import Any, Dict, Iterator, List

from .node import Node


class BreakNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[None]:
        yield


class ReturnNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[None]:
        yield
