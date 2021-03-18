from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Node(ABC):
    """Base node for AST"""
    __slots__ = ()

    @abstractmethod
    def children(self) -> List[Dict[str, Any]]:
        ...
