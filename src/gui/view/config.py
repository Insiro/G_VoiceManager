from PyQt6.QtWidgets import (
    QGridLayout,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
)
from locales import Lang
from src.gui.components import PathSelect, HLabeldCombo

from ..bin import GuiBin
from .view_base import ViewBase


class ConfigView(ViewBase):
    locale: HLabeldCombo

    def __init__(self, bin: GuiBin, parent: QWidget | None = None):
        ViewBase.__init__(self, bin=bin, parent=parent)
        self._conf = bin.conf_service

        self._layout = QVBoxLayout()
        self.locale = HLabeldCombo("Locale", [item.value for item in Lang], self)
        self.locale.combo.setCurrentText(self._conf.locale)
        self._layout.addWidget(self.locale)
        self.voice = HLabeldCombo("Voice", self._conf.voice_list, self)
        self.voice.combo.setCurrentText(self._conf.voice_lang)
        self._layout.addWidget(self.voice)
        self.setLayout(self._layout)
        self.init_path()
        self.init_bottom()

    def init_path(self):
        box = QGroupBox("path", self)
        layout = RowGridLayout(box)
        box.setLayout(layout)

        self.temp = PathSelect(self._conf.temp_path)
        self.resource = PathSelect(self._conf.resource_path)
        self.genshin = PathSelect(self._conf.genshin_path)
        self.source = PathSelect(self._conf.mod_sources_path)
        self.backup = PathSelect(self._conf.backup_path)
        self.source = PathSelect(self._conf.mod_sources_path)

        layout.addLabelRow("genshin", self.genshin)
        layout.addLabelRow("source", self.source)
        layout.addLabelRow("resource", self.resource)
        layout.addLabelRow("temp", self.temp)
        layout.addLabelRow("backup", self.backup)
        self._layout.addWidget(box)

    def init_bottom(self):
        reset_btn = QPushButton("reset")
        apply_btn = QPushButton("apply")
        reset_btn.clicked.connect(self.reset)
        apply_btn.clicked.connect(self.apply)
        lay = QHBoxLayout()
        lay.addWidget(reset_btn)
        lay.addWidget(apply_btn)
        self._layout.addLayout(lay)

    def reset(self):
        self.voice.combo.setCurrentText(self._conf.voice_lang)
        self.source.path = self._conf.mod_sources_path
        self.resource.path = self._conf.resource_path
        self.temp.path = self._conf.temp_path
        self.backup.path = self._conf.backup_path
        self.genshin.path = self._conf.genshin_path
        self.locale.combo.setCurrentText(Lang.fromStr(self._conf.locale).value)
        return self

    def apply(self):
        self._conf.voice_lang = self.voice.combo.currentText()
        self._conf.mod_sources_path = self.source.path
        self._conf.resource_path = self.resource.path
        self._conf.temp_path = self.temp.path
        self._conf.backup_path = self.backup.path
        self._conf.genshin_path = self.genshin.path
        self._conf.locale = Lang.fromStr(self.locale.combo.currentText()).name
        self._conf.commit()


class RowGridLayout(QGridLayout):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self._rows = 0

    def addLabelRow(self, text: str, widget: QWidget):
        self.addWidget(QLabel(text), self._rows, 1)
        self.addWidget(widget, self._rows, 2)
        self._rows += 1
