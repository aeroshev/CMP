class BadInputError(Exception):
    """Exceptions of None root"""
    def __init__(self, text: str = '') -> None:
        self.text = text
