from .node import Node


class ErrorNode(Node):
    """Node of error parsing"""

    __slots__ = "message"

    def __init__(self, message: str) -> None:
        self.message = message
