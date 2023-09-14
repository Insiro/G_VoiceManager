import typing
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QComboBox,
)
from src.gui.bin import Bin
from .view_base import ViewBase


class MainView(ViewBase):
    mod_ComboBox: QComboBox
    restore_combo: QComboBox

    def __init__(self, bin: Bin):
        super().__init__(bin)
        backup_btn = QPushButton("BackUp")
        backup_btn.clicked.connect(self.backup)

        vbox = QVBoxLayout()
        vbox.addWidget(self.initModGroup())
        vbox.addWidget(self.initRestoreGroup())
        vbox.addWidget(backup_btn)
        self.setLayout(vbox)

    def initModGroup(self):
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply)
        self.mod_ComboBox = QComboBox()
        self.reloadMods()
        self.mod_ComboBox.setPlaceholderText("--Select Mod--")
        self.mod_ComboBox.setCurrentIndex(-1)

        layout = QHBoxLayout()
        layout.addWidget(self.mod_ComboBox)
        layout.addWidget(apply_btn)
        bg = QGroupBox("Apply Mod")
        bg.setLayout(layout)
        return bg

    def initRestoreGroup(self):
        restore_btn = QPushButton("restore")
        restore_btn.clicked.connect(self.restore)
        self.restore_combo = QComboBox()
        self.restore_combo.addItems(["link", "move"])

        layout = QHBoxLayout()
        layout.addWidget(self.restore_combo)
        layout.addWidget(restore_btn)
        bg = QGroupBox("restore")
        bg.setLayout(layout)
        return bg

    def backup(self):
        self._bin.threading(
            self._service.isolate_original,
            "BackUp Finished",
            "Voice Not Installed or Sym link is Activated",
        )

    def restore(self):
        selected = self.restore_combo.currentText()
        work = lambda: self._service.restore(selected == "link")
        self._bin.threading(work, "Restore Success", "Restore Failed")

    def apply(self):
        idx = self.mod_ComboBox.currentIndex()
        if idx == 0:
            self.reloadMods()
            return
        mod_name = self.mod_ComboBox.currentText()
        self._service.apply(mod_name)

    def reloadMods(self):
        self.mod_ComboBox.clear()
        self.mod_ComboBox.addItem("refresh list")
        mod_list = self._service.get_applied_mods()
        self.mod_ComboBox.addItems(mod_list)

    def reset(self):
        self.mod_ComboBox.setCurrentIndex(-1)
        self.restore_combo.setCurrentIndex(0)
