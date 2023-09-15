from PyQt6.QtWidgets import QComboBox, QWidget
from .h_labeld_widget import HLabeldWidget


class HLabeldCombo(HLabeldWidget):
    @property
    def combo(self):
        return self._combo

    def __init__(
        self, label: str, options: list[str] = None, parent: QWidget | None = None
    ):
        self._combo = QComboBox(parent)
        super().__init__(label, parent)
        self.addWidget(self._combo)
        if options is not None:
            self._combo.addItems(options)
