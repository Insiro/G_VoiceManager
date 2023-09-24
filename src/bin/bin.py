from .mod_tool import ModTool
from .service import ModService
from .config import Config
import logging
import sys
from src.utils.logger import LoggerWriter


class Bin:
    @property
    def service(self):
        return self._service

    @property
    def logger(self):
        return self.__logger

    def __init__(self, config: Config, logConsole=False, *args, **kwargs) -> None:
        logger = self.init_logger(logConsole)
        tool = ModTool(config, logger)
        self._service = ModService(tool)
        self.__logger = logger

    def init_logger(self, logConsole):
        logger = logging.getLogger()

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stderr_log_handler = logging.StreamHandler()
        stderr_log_handler.setFormatter(formatter)
        file_log_handler = logging.FileHandler("GVM.log", "a", encoding="utf-8")
        file_log_handler.setFormatter(formatter)
        if logConsole:
            logger.addHandler(stderr_log_handler)
        logger.addHandler(file_log_handler)

        sys.stdout = LoggerWriter(logging.debug)
        sys.stderr = LoggerWriter(logging.warn)

        return logger
