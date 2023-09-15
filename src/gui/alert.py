from PyQt6.QtWidgets import (
    QCheckBox,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from .bin import Config


class Alert(QWidget):
    dno: QCheckBox

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.agree = False
        self.config = config
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.dno = QCheckBox("Do Not Open More", self)
        cancel_btn = QPushButton("cancel")
        cancel_btn.clicked.connect(self.cancel)
        ok_btn = QPushButton("agree")
        ok_btn.setProperty("class", "danger")
        ok_btn.clicked.connect(self.ok)

        self._layout.addWidget(
            QLabel(
                "no responsible for any problems that arise from using this software."
            )
        )
        self._layout.addWidget(
            QLabel(
                "Recomment to set backup dicectory on same disk where Game Data Saved"
            )
        )
        self._layout.addWidget(QLabel("created by github.com/Insiro"))

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
