from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QWidget,
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
        self._lang = QLabel()
        layout = QVBoxLayout()

        # region Current Language
        row_lang = QHBoxLayout()
        row_lang.addWidget(QLabel("Language"))
        row_lang.addWidget(self._lang)
        layout.addLayout(row_lang)
        # endregion

        # region Current ModState
        row_state = QHBoxLayout()
        row_state.addWidget(QLabel("Mod State"))
        row_state.addWidget(self._state)
        layout.addLayout(row_state)
        # endregion

        # region Persist
        self._persist = QWidget()
        self._persist.setLayout(QHBoxLayout())
        rm_persist_btn = QPushButton("Remove")
        rm_persist_btn.setProperty("class", "danger")
        rm_persist_btn.setProperty("flat", "true")
        rm_persist_btn.setStyleSheet("text-align:left;")
        rm_persist_btn.clicked.connect(self.removePersistant)
        self._persist.layout().addWidget(QLabel("Persistant Exist"))
        self._persist.layout().addWidget(rm_persist_btn)
        layout.addWidget(self._persist)
        # endregion

        self.setLayout(layout)
        self.updateState()

    def updateState(self):
        self._lang.setText(self._bin.conf_service.voice_lang)
        state = ""
        if not self._service.exist_voice:
            state = self._locale["removed"]
        elif act := self._service.is_activated_original_and_link:
            if act == 1:
                state = f"{self._locale['original']} {self._locale['link']} {self._locale['activated']}"
            else:
                state = self._locale["no_backup"]
        else:
            state = self._service.current_mod + f" {self._locale['activated']}"

        self._state.setText(state)

        # Update Persistant State
        self._persist.setVisible(self._service.exist_persistant)

    def removePersistant(self):
        def rmjob():
            self._service.delete_persistant()
            self.updateState()

        self._bin.threading(rmjob)


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
        def backup_job():
            self._service.isolate_original()
            self.reset()

        self._bin.threading(
            backup_job,
            f"{self._locale['main']['backup']} {self._locale['success']}",
            self._locale["main"]["backup_fail"],
        )

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
        self._bin.logger.info(f"apply mod {mod_name}")
        try:
            self._service.apply(mod_name)
        except NotValidSymLinkException as e:
            self._bin.logger.error("cnnot find symlink")
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
