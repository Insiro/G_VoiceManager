from abc import abstractmethod
from PyQt6.QtWidgets import QWidget

from src.gui.bin.bin import Bin


class ViewBase(QWidget):
    def __init__(self, bin: Bin):
        super().__init__()
        self._bin = bin
        self._locale = bin.locale
        self._service = bin.service

    @abstractmethod
    def reset(self):
        raise NotImplementedError()
        pass
