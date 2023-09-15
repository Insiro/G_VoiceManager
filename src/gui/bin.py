from typing import Any, Callable

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QWidget

from locales import locale
from src.bin import Bin, Config, ConfigService

from ..gui.components import ErrorModal, Modal, ProcessOverlay, Worker


class GuiBin(QObject):
    @property
    def service(self):
        return self._bin.service

    @property
    def conf_service(self):
        return self._conf_service

    @property
    def process_overlay(self):
        return self.__overlay

    @property
    def root(self):
        return self.__root

    @property
    def modal(self):
        return self.__error_modal

    @property
    def config(self):
        return self._config

    def __init__(self, config: Config, root: QWidget | None = None) -> None:
        self._bin = Bin(config)
        self.__root = root
        self._config = config
        self.locale = locale(config.locale)
        self._conf_service = ConfigService(config)

    def connectApp(self, root: QWidget):
        if self.__root is not None:
            return
        super().__init__(root)
        self.__root = root
        self.__overlay = ProcessOverlay(root)
        self.__error_modal = ErrorModal(root)
        self.__modal = Modal(root)
        self.__worker = Worker(root)
        self.__worker.fisnish.connect(self._finishWork)
        self.__worker.error.connect(self._openErrorModal)

    @pyqtSlot(str)
    def _openErrorModal(self, msg: str):
        self.__overlay.stop()
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
