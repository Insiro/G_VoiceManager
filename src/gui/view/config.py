from PyQt6 import QtWidgets
from src.bin import GuiBin
from .view_base import ViewBase


class ConfigView(ViewBase):
    def __init__(self, bin: GuiBin):
        super().__init__(bin)
        self.list_view = QtWidgets.QListWidget()
        self.list_view.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.list_view.addItems(
            ["Select Base Mod", "add Mod Source", "Clear Inputs", "Pack Mod"]
        )
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.list_view)
        self.setLayout(vbox)

    def reset(self):
        pass
