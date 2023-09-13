from PyQt6 import QtWidgets
from src.service import ModService


class ConfigView(QtWidgets.QWidget):
    def __init__(self, service: ModService):
        super().__init__()
        self.service = service

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
