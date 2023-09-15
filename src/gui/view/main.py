from PyQt6.QtWidgets import (
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
        apply_btn = QPushButton(self._locale["apply"])
        apply_btn.clicked.connect(self.apply)
        self.mod_ComboBox = QComboBox()
        self.reloadMods()
        self.mod_ComboBox.setPlaceholderText(self._locale["main"]["select_mod"])
        self.mod_ComboBox.setCurrentIndex(-1)

        layout = QHBoxLayout()
        layout.addWidget(self.mod_ComboBox)
        layout.addWidget(apply_btn)
        bg = QGroupBox(self._locale["main"]["apply_mod"])
        bg.setLayout(layout)
        return bg

    def initRestoreGroup(self):
        restore_btn = QPushButton(self._locale["main"]["restore"])
        restore_btn.clicked.connect(self.restore)
        self.restore_combo = QComboBox()
        self.restore_combo.addItems(
            [self._locale["main"]["link"], self._locale["main"]["move"]]
        )

        layout = QHBoxLayout()
        layout.addWidget(self.restore_combo)
        layout.addWidget(restore_btn)
        bg = QGroupBox(self._locale["main"]["restore"])
        bg.setLayout(layout)
        return bg

    def backup(self):
        self._bin.threading(
            self._service.isolate_original,
            f"{self._locale['main']['backup']} {self._locale['success']}",
            self._locale["main"]["backup_fail"],
        )

    def restore(self):
        selected = self.restore_combo.currentText()
        work = lambda: self._service.restore(selected == self._locale["main"]["link"])
        self._bin.threading(
            work,
            self._locale["main"]["restore"] + " " + self._locale["success"],
            self._locale["main"]["restore"] + " " + self._locale["failed"],
        )

    def apply(self):
        if 0 == self.mod_ComboBox.currentIndex():
            self.reloadMods()
            return
        mod_name = self.mod_ComboBox.currentText()
        self._service.apply(mod_name)

    def reloadMods(self):
        self.mod_ComboBox.clear()
        self.mod_ComboBox.addItem(self._locale["refresh"])
        mod_list = self._service.get_applied_mods()
        self.mod_ComboBox.addItems(mod_list)

    def reset(self):
        self.mod_ComboBox.setCurrentIndex(-1)
        self.restore_combo.setCurrentIndex(0)
