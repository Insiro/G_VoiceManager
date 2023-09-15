from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QFileDialog,
    QLineEdit,
    QWidget,
    QHBoxLayout,
)


class PathSelect(QWidget):
    @property
    def path(self):
        return self._path.text()

    @path.setter
    def path(self, path: str):
        self._path.setText(path)

    def __init__(self, current: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        dialog_btn = QPushButton("Select")
        dialog_btn.clicked.connect(self.showDialog)
        lay = QHBoxLayout()
        self.setLayout(lay)
        self._path = QLineEdit(current)
        lay.addWidget(self._path)
        lay.addWidget(dialog_btn)

    def showDialog(self):
        dir = QFileDialog.getExistingDirectory(None, "Open folder", self._path.text())
        self._path.setText(dir)
