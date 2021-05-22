class Singleton:
    """
    Base class for release pattern Singleton
    """
    _instances = None  # type: object

    def __new__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances = super().__new__(cls, *args, **kwargs)
        return cls._instances
