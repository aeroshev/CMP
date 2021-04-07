from abc import ABC
from typing import Iterator


class Node(ABC):
    """Base node for AST"""
    __slots__ = ()

    def __iter__(self) -> Iterator['Node']:
        yield self

    def __len__(self) -> int:
        return len(self.__slots__)

    def __str__(self) -> str:
        return self.__class__.__name__
