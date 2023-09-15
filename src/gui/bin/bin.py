from PyQt6.QtCore import pyqtSlot, QObject
from PyQt6.QtWidgets import QWidget
from locales import locale

from src.service import ModService

from src.gui.components import ErrorModal, ProcessOverlay, Modal
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
        return self.__error_modal

    def __init__(self, root: QWidget, service: ModService) -> None:
        super().__init__(root)
        self.__root = root
        self.__service = service
        self.__overlay = ProcessOverlay(root)
        self.__error_modal = ErrorModal(root)
        self.__modal = Modal(root)
        self.__worker = Worker(root)
        self.locale = locale(service._config.lang)

        self.__worker.fisnish.connect(self._finishWork)
        self.__worker.error.connect(self._openErrorModal)

    @pyqtSlot(str)
    def _openErrorModal(self, msg: str):
        self.__error_modal.msg = msg
        self.__error_modal.show()

    @pyqtSlot()
    def _finishWork(self):
        self.__overlay.stop()
        if self.__display_msg:
            self.__modal.show()

    def threading(
        self,
        work: Callable[[], Any],
        success_msg: str | None = None,
        fail_msg: str | None = None,
    ):
        self.__worker.work = work
        self.__overlay.start()
        self.__worker.start()
        self.__worker.fail_msg = fail_msg
        self.__display_msg = success_msg is not None
        self.__modal.msg = success_msg

    def show_modal(self, msg: str | None):
        self.__display_msg = True
        self.__modal.msg = msg
        self.__modal.show()
