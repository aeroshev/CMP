from abc import ABC, abstractmethod
from typing import Any, List, Union


class EmptyNode:
    """"""
    __slots__ = ()

    def __add__(self, other: Any) -> Any:
        return other

    def __iter__(self):
        yield self


class Node(ABC):
    """Base node for AST"""
    __slots__ = ()

    @abstractmethod
    def children(self) -> List[Any]:
        ...

    @abstractmethod
    def __iter__(self):
        ...

    def __len__(self) -> int:
        return len(self.__slots__)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __add__(self, other: 'Node') -> Union['Node', List['Node']]:  # TODO rebuild to radd
        if isinstance(self, EmptyNode):
            return other
        elif isinstance(other, EmptyNode):
            return self
        else:
            return [self, other]
