from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
from src.gui.bin import GuiBin
from .view_base import ViewBase


class ModView(ViewBase):
    def __init__(self, bin: GuiBin, parent: QWidget | None = None):
        super().__init__(bin, parent)
        self._layout = QVBoxLayout(self)
        self._locale = bin.locale
        self.listview = QListWidget(self)
        self.setLayout(self._layout)
        btn = QPushButton("Delete", self)
        btn.clicked.connect(self._delete_items)

        self._layout.addWidget(self.listview)
        self._layout.addWidget(btn)

    def reset(self):
        self.listview.clear()
        self.listview.addItems(self._service.get_applied_mods())

    def _delete_items(self):
        selected = self.listview.currentItem().text()
        job = lambda: self._service.delete_mod(selected)
        self._bin.threading(
            job, f"{selected} {self._locale['mod']['delete']} {self._locale['success']}"
        )
