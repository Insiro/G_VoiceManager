from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget, QLayout


class HLabeldWidget(QWidget):
    def __init__(
        self,
        label: str,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(QLabel(label))

    def layout(self):
        return self._layout

    def addWidget(self, widget: QWidget):
        self._layout.addWidget(widget)

    def addLayout(self, layout: QLayout):
        self._layout.addLayout(layout)
