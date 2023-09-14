from src.service import ModService
from src.utils.error import ModManagerException
from .process_overlay import ProcessOverlay
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QThread, QEventLoop
from typing import Callable
from .error_modal import ErrorModal


class Bin:
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
        self.__root = root
        self.__service = service
        self.__overlay = ProcessOverlay(root)
        self.__modal = ErrorModal(root)
        pass

    def getWorker(self, work: Callable[[], None]):
        return Worker(self, work)


class Worker(QThread):
    def __init__(self, bin: Bin, work: Callable[[], None], fail_msg=None) -> None:
        super().__init__(bin.root)
        self.modal = bin.modal
        self.__overlay = bin.process_overlay
        self.work = work
        self.fail_msg = fail_msg

    def run(self):
        self.__overlay.disableParentDuringLoading(self)
        self.__overlay.start()
        try:
            self.work()
        except ModManagerException as e:
            msg = e.get_msg if self.fail_msg is None else self.fail_msg
            self._displayErrorModal(msg)

        except Exception as e:
            msg = "UnExpected Error : " + e.__class__.__name__
            self._displayErrorModal(msg)
            self.__overlay.stop()
            exit()
        finally:
            self.__overlay.stop()

    def _displayErrorModal(self, msg: str):
        self.modal.msg = msg
        self.modal.showNormal()
        loop = QEventLoop()
        self.modal.destroyed.connect(loop.quit)
        loop.exec()  # wait ..
