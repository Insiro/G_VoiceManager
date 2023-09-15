from PyQt6.QtWidgets import (
    QCheckBox,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from .bin import GuiBin


class Alert(QWidget):
    dno: QCheckBox

    def __init__(self, bin: GuiBin) -> None:
        super().__init__()
        self.agree = False
        self.config = bin.config
        locale = bin.locale
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.dno = QCheckBox(locale["alert"]["hide"], self)
        cancel_btn = QPushButton(locale["alert"]["cancel"])
        cancel_btn.clicked.connect(self.cancel)
        ok_btn = QPushButton(locale["alert"]["argree"])
        ok_btn.setProperty("class", "danger")
        ok_btn.clicked.connect(self.ok)
        self._layout.addWidget(QLabel(" "))
        self._layout.addWidget(QLabel(locale["alert"]["responbility"]))
        self._layout.addWidget(QLabel(" "))

        self._layout.addWidget(self.dno, alignment=Qt.AlignmentFlag.AlignRight)
        hbox = QHBoxLayout()
        hbox.addWidget(cancel_btn)
        hbox.addWidget(ok_btn)
        self._layout.addLayout(hbox)

    def ok(self):
        self.agree = True
        if self.dno.isChecked():
            self.config.hide = True
            self.config.save()
        self.close()

    def cancel(self):
        self.agree = False
        self.close()
