from abc import abstractmethod
from PyQt6.QtWidgets import QWidget

from src.bin import GuiBin


class ViewBase(QWidget):
    def __init__(self, bin: GuiBin, parent: QWidget | None = None):
        super().__init__(parent)
        self._bin = bin
        self._locale = bin.locale
        self._service = bin.service

    @abstractmethod
    def reset(self):
        raise NotImplementedError()
