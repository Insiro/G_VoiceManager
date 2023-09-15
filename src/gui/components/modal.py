from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class Modal(QDialog):
    @property
    def msg(self):
        return self._msg.text()

    @msg.setter
    def msg(self, message: str):
        self._msg.setText(message)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._msg = QLabel()
        close_btn = QPushButton("close")
        close_btn.clicked.connect(self.hide)
        layout = QVBoxLayout()
        layout.addWidget(self._msg)
        layout.addWidget(close_btn)
        self.setLayout(layout)


class ErrorModal(QDialog):
    @property
    def msg(self):
        return self._msg.text()

    @msg.setter
    def msg(self, message: str):
        self._msg.setText(message)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._msg = QLabel()
        close_btn = QPushButton("close")
        close_btn.clicked.connect(self.hide)
        layout = QVBoxLayout()
        layout.addWidget(self._msg)
        layout.addWidget(close_btn)
        self.setLayout(layout)
