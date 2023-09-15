from PyQt6.QtWidgets import QPushButton, QWidget, QLabel, QFileDialog, QLineEdit
from .h_labeld_widget import HLabeldWidget


class HLabeldPath(HLabeldWidget):
    @property
    def path(self):
        return self._path.text()

    @path.setter
    def path(self, path: str):
        self._path.setText(path)

    def __init__(self, label: str, current: str = "", parent: QWidget | None = None):
        super().__init__(label, parent)

        self._path = QLineEdit(current)
        self.setProperty("class", "secondary")
        dialog_btn = QPushButton("Select")
        dialog_btn.clicked.connect(self.showDialog)
        self.addWidget(self._path)
        self.addWidget(dialog_btn)

    def showDialog(self):
        dir = QFileDialog.getExistingDirectory(None, "Open folder", self._path.text())
        self._path.setText(dir)
