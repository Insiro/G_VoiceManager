from typing import Callable

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget

from src.utils.error import ModManagerException

import traceback


class Worker(QThread):
    work: Callable[[], None] | None = None
    fail_msg: str | None = None
    error = pyqtSignal(str)
    fisnish = pyqtSignal()

    def __init__(self, root: QWidget) -> None:
        super().__init__(root)

    def run(self):
        if self.work is None:
            return
        try:
            self.work()
            self.fisnish.emit()
        except ModManagerException as e:
            msg = e.get_msg() if self.fail_msg is None else self.fail_msg
            self.error.emit(msg)
        except Exception as e:
            msg = "UnExpected Error : " + e.__class__.__name__
            print(traceback.format_exc())
            self.error.emit(msg)
        finally:
            self.work = None
