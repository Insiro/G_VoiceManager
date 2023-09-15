from PyQt6.QtWidgets import QWidget
from .h_labeld_widget import HLabeldWidget
from ..path_select import PathSelect


class HLabeldPath(HLabeldWidget):
    @property
    def path(self):
        return self._path.path

    @path.setter
    def path(self, path: str):
        self._path.path = path

    def __init__(self, label: str, current: str = "", parent: QWidget | None = None):
        super().__init__(label, parent)

        self._path = PathSelect(current, parent)
        self.addWidget(self._path)
