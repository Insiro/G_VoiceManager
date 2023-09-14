from PyQt6.QtCore import pyqtSlot, QObject
from PyQt6.QtWidgets import QWidget

from src.service import ModService

from .error_modal import ErrorModal
from .process_overlay import ProcessOverlay
from .worker import Worker
from typing import Callable, Any


class Bin(QObject):
    @property
    def service(self):
        return self.__service

    @property
    def process_overlay(self):
        return self.__overlay

    @property
    def root(self):
        return self.__root

    @property
    def modal(self):
        return self.__modal

    def __init__(self, root: QWidget, service: ModService) -> None:
        super().__init__(root)
        self.__root = root
        self.__service = service
        self.__overlay = ProcessOverlay(root)
        self.__modal = ErrorModal(root)
        self.__worker = Worker(root)

        # connect worker slot
        self.__worker.fisnish.connect(self._finishWork)
        self.__worker.error.connect(self._openErrorModal)

    @pyqtSlot(str)
    def _openErrorModal(self, msg: str):
        self.__modal.msg = msg
        self.__modal.show()

    @pyqtSlot()
    def _finishWork(self):
        self.__overlay.stop()

    def threading(self, work: Callable[[], Any], fail_msg: str | None = None):
        self.__worker.work = work
        self.__overlay.start()
        self.__worker.start()
        self.__worker.fail_msg = fail_msg
