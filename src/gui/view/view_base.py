from abc import ABCMeta, abstractmethod
from PyQt6.QtWidgets import QWidget

from src.gui.bin.bin import Bin


class ViewBase(QWidget):
    def __init__(self, bin: Bin):
        super().__init__()
        self._bin = bin
        self._service = bin.service

    @abstractmethod
    def reset(self):
        self.select_base.reset()
        self.source_list.reset()
        self._edit_mod_name.clear()
