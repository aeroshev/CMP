from abc import abstractmethod
from typing import Any, Dict, List

from .node import Node


class ConditionalNode(Node):
    """"""
    __slots__ = "main_statement"

    def __init__(self, main_stmt: Node) -> None:
        self.main_statement = main_stmt

    @abstractmethod
    def children(self) -> List[Dict[str, Any]]:
        ...


class SimpleConditionalNode(ConditionalNode):
    """"""
    __slots__ = ("main_statement", "statements_list")

    def __init__(self, main_stmt: Node, stmt_list: List[Node]) -> None:
        super().__init__(main_stmt)
        self.statements_list = stmt_list

    def children(self) -> List[Dict[str, Any]]:
        ...


class TwoBranchConditionalNode(ConditionalNode):
    """"""
    __slots__ = ("main_statement", "main_branch", "alternative_branch")

    def __init__(
            self,
            main_stmt: Node,
            main_branch: List[Node],
            alt_branch: List[Node]
    ) -> None:
        super().__init__(main_stmt)
        self.main_branch = main_branch
        self.alternative_branch = alt_branch

    def children(self) -> List[Dict[str, Any]]:
        ...
#
#
# class ManyBranchConditionalNode(ConditionalNode):
#     """"""
#     __slots__ = ("main_statement", "main_branch", "alternative_branch")
