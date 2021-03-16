from abc import ABC, abstractmethod


class Node(ABC):
    """Base node for AST"""
    __slots__ = ()

    @abstractmethod
    def children(self):
        ...
