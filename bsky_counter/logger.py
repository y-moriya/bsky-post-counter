from logging import config, getLogger, Logger, DEBUG, INFO


class BskyCounterLogger:
    _LOGGER_NAME = "BskyCounterLogger"
    _CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d#%(funcName)s]: %(message)s"
            }
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "simple"
            }
        },
        "loggers": {
            _LOGGER_NAME: {
                "level": "WARN",
                "handlers": ["consoleHandler"]
            }
        },
    }
    _logger: Logger

    def __init__(self, info: bool = False, debug: bool = False):
        config.dictConfig(self._CONFIG)
        self._logger = getLogger("BskyCounterLogger")
        if info:
            self._logger.setLevel(INFO)
        if debug:
            self._logger.setLevel(DEBUG)

    def get_logger(self) -> Logger:
        return self._logger
