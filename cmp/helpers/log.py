import logging


class LogMixin:
    """
    Class mixin for produce
    logger entire class
    """
    # logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG,
        filename="parselog.txt",
        filemode="w",
        format="%(filename)10s:%(lineno)4d:%(message)s"
    )

    @property
    def logger(self) -> logging.Logger:
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)
