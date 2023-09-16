from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from src.utils.error import NotValidSymLinkException
from ..bin import GuiBin
from .view_base import ViewBase


class Header(QGroupBox):
    def __init__(self, bin: GuiBin):
        super().__init__()
        self._bin = bin
        self._service = bin.service
        self._locale = bin.locale["main"]
        self._state = QLabel()
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Mod State"))
        layout.addWidget(self._state)
        self.setLayout(layout)
        self.updateState()

    def updateState(self):
        if not self._service.exist_voice:
            self._state.setText(self._locale["removed"])
            return
        if act := self._service.is_activated_original_and_link:
            self._state.setText(
                f"{self._locale['original']} "
                + f"{self._locale['link']} {self._locale['activated']}"
                if act == 1
                else self._locale["no_backup"]
            )

            return
        self._state.setText(self._service.current_mod + f" {self._locale['activated']}")


class MainView(ViewBase):
    mod_ComboBox: QComboBox
    restore_combo: QComboBox

    def __init__(self, bin: GuiBin):
        super().__init__(bin)
        backup_btn = QPushButton("BackUp")
        backup_btn.clicked.connect(self.backup)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.header = Header(self._bin)
        vbox.addWidget(self.header)

        vbox.addWidget(self.initModGroup())
        vbox.addWidget(self.initRestoreGroup())
        vbox.addWidget(backup_btn)

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
            self.backup_job,
            f"{self._locale['main']['backup']} {self._locale['success']}",
            self._locale["main"]["backup_fail"],
        )

    def backup_job(self):
        self._service.isolate_original()
        self.reset()

    def restore(self):
        self._bin.threading(
            self.restoreWork,
            self._locale["main"]["restore"] + " " + self._locale["success"],
            self._locale["main"]["restore"] + " " + self._locale["failed"],
        )

    def restoreWork(self):
        selected = self.restore_combo.currentText()
        self._service.restore(selected == self._locale["main"]["link"])
        self.reset()

    def apply(self):
        if 0 == self.mod_ComboBox.currentIndex():
            self.reloadMods()
            return
        mod_name = self.mod_ComboBox.currentText()
        print(mod_name)
        try:
            self._service.apply(mod_name)
        except NotValidSymLinkException as e:
            self._bin.show_modal("cannot find symlink")
        self.reset()

    def reloadMods(self):
        self.mod_ComboBox.clear()
        self.mod_ComboBox.addItem(self._locale["refresh"])
        mod_list = self._service.get_applied_mods()
        self.mod_ComboBox.addItems(mod_list)

    def reset(self):
        self.header.updateState()
        self.reloadMods()
        self.mod_ComboBox.setCurrentIndex(-1)
        self.restore_combo.setCurrentIndex(0)
