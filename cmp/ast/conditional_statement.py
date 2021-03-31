from abc import abstractmethod
from itertools import chain
from typing import Any, Dict, Iterator, List

from .node import Node


class ConditionalNode(Node):
    """"""
    __slots__ = "main_stmt"

    def __init__(self, main_stmt: Node) -> None:
        self.main_stmt = main_stmt

    @abstractmethod
    def children(self) -> List[Dict[str, Any]]:
        ...


class SimpleConditionalNode(ConditionalNode):
    """
    Conditional node for one way statement
    >>> if (expression is True)
    >>>         do_something
    """
    __slots__ = ("main_statement", "statements_list")

    def __init__(self, main_stmt: Node, stmt_list: List[Node]) -> None:
        super().__init__(main_stmt)
        self.stmt_list = stmt_list

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[Node]:
        yield self.main_stmt
        for stmt in self.stmt_list:
            yield stmt


class TwoBranchConditionalNode(ConditionalNode):
    """
    Conditional node for two way statement
    >>> if (expression is True)
    >>>         do_something
    >>> else
    >>>         to_do
    """
    __slots__ = ("main_stmt", "main_branch", "alt_branch")

    def __init__(
            self,
            main_stmt: Node,
            main_branch: List[Node],
            alt_branch: List[Node]
    ) -> None:
        super().__init__(main_stmt)
        self.main_branch = main_branch
        self.alt_branch = alt_branch

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[Node]:
        for stmt in chain(self.main_stmt, self.main_branch, self.alt_branch):
            yield stmt

#
#
# class ManyBranchConditionalNode(ConditionalNode):
#     """"""
#     __slots__ = ("main_statement", "main_branch", "alternative_branch")
