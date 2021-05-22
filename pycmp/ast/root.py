from typing import Iterator

from .node import Node


class FileAST(Node):
    """Entry point in AST"""
    __slots__ = "root"

    def __init__(self, root: Node) -> None:
        self.root = root

    def __iter__(self) -> Iterator[Node]:
        for stmt in self.root:
            yield stmt
