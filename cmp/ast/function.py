from typing import Any, Dict, Iterator, List

from .node import Node


class FunctionNode(Node):
    """"""
    __slots__ = ("declare", "body")

    def __init__(self, declare: Node, body: List[Node]) -> None:
        self.declare = declare
        self.body = body

    def children(self) -> List[Dict[str, Any]]:
        ...

    def __iter__(self) -> Iterator[Node]:
        yield self.declare
        for stmt in self.body:
            yield stmt
