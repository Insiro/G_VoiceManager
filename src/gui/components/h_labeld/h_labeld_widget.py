from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class HLabeldWidget(QHBoxLayout):
    def __init__(
        self,
        label: str,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.addWidget(QLabel(label))
