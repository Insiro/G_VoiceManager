from os import path

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from src.bin import assetSub

from .bin import GuiBin
from .components import HLabeldPath, Modal


class GPathFix(QWidget):
    def __init__(self, bin: GuiBin, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.passed = False
        self.bin = bin
        locale = bin.locale
        gp_str = f"{locale['setting']['genshin']} {locale['alert']['path']}"
        self.pselect = HLabeldPath(gp_str, parent=self)
        self.btn = QPushButton(locale["save"])
        self.btn.clicked.connect(self.onclick)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{gp_str} {locale['wrong']}"))
        layout.addWidget(self.pselect)
        layout.addWidget(self.btn)
        self.setLayout(layout)
        self.modal = Modal(self)
        self.modal.msg = (
            f"Selected {gp_str} {locale['wrong']} {locale['alert']['cannotFindVoice']}"
        )
        self.setMinimumWidth(500)

    def onclick(self):
        gpath = self.pselect.path
        if path.isdir(path.join(gpath, assetSub)):
            print(path.join(gpath, assetSub))
            self.bin.config.genshin_path = gpath
            self.bin.config.save()
            self.passed = True
            self.close()
            return
        self.modal.show()
