from PyQt6 import QtWidgets
from src.gui.bin import Bin


class ConfigView(QtWidgets.QWidget):
    def __init__(self, bin: Bin):
        super().__init__()
        self.service = bin.service

        self.canvas = None
        self.list_view = None
        self.image_label = None
        self.setLayout(self.content())

    def content(self):
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
        return vbox
