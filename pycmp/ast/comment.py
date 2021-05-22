from .node import Node


class CommentNode(Node):
    """ """
    __slots__ = "comment"

    def __init__(self, comment: str) -> None:
        self.comment = comment
