import logging


class LogMixin:
    """
    Class mixin for produce
    logger entire class
    """
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    @property
    def logger(self) -> logging.Logger:
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)
