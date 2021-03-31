from typing import Any, Dict, Iterator, List

from .node import Node


class PlusUnaryNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[None]:
        yield


class MinusUnaryNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[None]:
        yield


class NegativeUnaryNode(Node):
    """"""
    __slots__ = ()

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[None]:
        yield
