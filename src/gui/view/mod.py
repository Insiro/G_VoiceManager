from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
from src.gui.bin import GuiBin
from .view_base import ViewBase
from os import startfile, path


class ModView(ViewBase):
    def __init__(self, bin: GuiBin, parent: QWidget | None = None):
        super().__init__(bin, parent)
        self._layout = QVBoxLayout(self)
        self._locale = bin.locale
        self.listview = QListWidget(self)
        self.setLayout(self._layout)
        btn = QPushButton("Delete", self)
        btn.clicked.connect(self._delete_items)
        folderBtn = QPushButton("open folder")
        folderBtn.clicked.connect(
            lambda: startfile(path.realpath(self._bin.config.packed_mods_path))
        )

        self._layout.addWidget(self.listview)
        self._layout.addWidget(btn)
        self._layout.addWidget(folderBtn)

    def reset(self):
        self.listview.clear()
        self.listview.addItems(self._service.get_applied_mods())

    def _delete_items(self):
        selected = self.listview.currentItem()
        if selected is None:
            self._bin.show_modal(
                f"{self._locale['item']} {self._locale['notselected']}"
            )
            return
        self._bin.threading(
            self._delete_work,
            f"{selected.text()} {self._locale['mod']['delete']} {self._locale['success']}",
        )

    def _delete_work(self):
        self._bin.process_overlay.desc_text = "deleting"
        selected = self.listview.currentItem().text()
        self._service.delete_mod(selected)
        self.reset()
