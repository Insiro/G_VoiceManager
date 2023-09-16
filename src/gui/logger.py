import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


class LoggerWriter:
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != "\n":
            self.level(message)

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)


# Create Logger if doesn't exist


def setLogging():
    dir = "./log"
    if not os.path.isdir(dir):
        os.mkdir(dir)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = TimedRotatingFileHandler(
        os.path.join(dir, "error.log"), when="midnight", interval=1, encoding="utf8"
    )
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    sys.stdout = LoggerWriter(logging.debug)
    sys.stderr = LoggerWriter(logging.warning)
