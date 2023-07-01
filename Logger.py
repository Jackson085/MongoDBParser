import logging


def _build_log_handler():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(module)s]')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler


class Logger:
    def __init__(self, log_level: int = logging.DEBUG):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.addHandler(_build_log_handler())
