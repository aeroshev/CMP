from abc import abstractmethod
from typing import Any, Dict, Iterator, List

from .node import Node


class ConditionalNode(Node):
    """"""
    __slots__ = "main_stmt"

    def __init__(self, main_stmt: Node) -> None:
        self.main_stmt = main_stmt


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

#
#
# class ManyBranchConditionalNode(ConditionalNode):
#     """"""
#     __slots__ = ("main_statement", "main_branch", "alternative_branch")
