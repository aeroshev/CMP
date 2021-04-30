import logging
import os


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


class ServerLog:
    """
    Custom logger for TCP server
    """
    def __init__(self, name: str = 'server'):
        self.logger = logging.getLogger(name)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.abspath('server.log'))
        file_handler.setLevel(logging.INFO)

        stream_format = logging.Formatter('%(message)s')
        file_format = logging.Formatter('%(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_format)
        file_handler.setFormatter(file_format)

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
