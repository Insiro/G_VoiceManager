from PyQt6 import QtWidgets
from src.gui.bin import Bin
from .view_base import ViewBase


class ConfigView(ViewBase):
    def __init__(self, bin: Bin):
        super().__init__(bin)
        vbox = QtWidgets.QVBoxLayout()
        self.list_view = QtWidgets.QListWidget()
        self.list_view.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        vbox.addWidget(self.list_view)
        self.list_view.addItems(
            ["Select Base Mod", "add Mod Source", "Clear Inputs", "Pack Mod"]
        )
        self.setLayout(vbox)
