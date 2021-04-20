from typing import List

from .node import Node


class ConditionalNode(Node):
    """Base node for conditional statements"""
    __slots__ = "main_stmt"

    def __init__(self, main_stmt: Node) -> None:
        self.main_stmt = main_stmt


class SimpleConditionalNode(ConditionalNode):
    """
    Conditional node for one way statement
    >>> if (expression is True)
    >>>         do_something
    """
    __slots__ = ("main_stmt", "stmt_list")

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


class ElseIfClauseNode(ConditionalNode):
    """Node of elseif clause"""
    __slots__ = ("main_stmt", "stmt_list")

    def __init__(self, main_stmt: Node, stmt_list: List[Node]) -> None:
        super().__init__(main_stmt=main_stmt)
        self.stmt_list = stmt_list


class ManyBranchConditionalNode(ConditionalNode):
    """Node of many conditional statement"""
    __slots__ = ("main_stmt", "main_branch", "alt_chain", "alt_branch")

    def __init__(
            self,
            main_stmt: Node,
            main_branch: List[Node],
            alt_chain: List[Node],
            alt_branch: List[Node]
    ) -> None:
        super().__init__(main_stmt=main_stmt)
        self.main_branch = main_branch
        self.alt_chain = alt_chain
        self.alt_branch = alt_branch
