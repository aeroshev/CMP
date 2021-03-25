from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Union


class EmptyNode:
    """"""
    __slots__ = ()

    def __add__(self, other: Any) -> Any:
        return other


class Node(ABC):
    """Base node for AST"""
    __slots__ = ()

    @abstractmethod
    def children(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator:
        ...

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __add__(self, other: 'Node') -> Union['Node', List['Node']]:  # TODO rebuild to radd
        if isinstance(self, EmptyNode):
            return other
        elif isinstance(other, EmptyNode):
            return self
        else:
            return [self, other]
