from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from src.gui.components import HLabeldCombo

from ..bin import GuiBin
from .view_base import ViewBase


class SelectSources(QGroupBox):
    @property
    def selectedItem(self) -> list[str]:
        return [item.text() for item in self._source_list.selectedItems()]

    def __init__(self, bin: GuiBin) -> None:
        super().__init__()
        self._locale = bin.locale
        self.setTitle(self._locale["genmods"]["source_select"])
        self._service = bin.service

        self._source_list = QListWidget()
        self._source_list.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self._source_list.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        refresh_btn = QPushButton(self._locale["refresh"])
        refresh_btn.clicked.connect(self._refresh_mod_list)

        layout = QVBoxLayout()
        layout.addWidget(self._source_list)
        layout.addWidget(refresh_btn)
        self._refresh_mod_list()
        self.setLayout(layout)

    def _refresh_mod_list(self):
        self.mod_sources = self._service.get_mod_sources()
        self._source_list.clear()

        for source in self.mod_sources:
            item = QListWidgetItem(source)
            self._source_list.addItem(item)

    def reset(self):
        self._source_list.reset()


class SelectBaseMod(HLabeldCombo):
    def __init__(self, bin: GuiBin):
        self._locale = bin.locale
        self._service = bin.service
        super().__init__(self._locale["genmods"]["mod_base"])
        self._combo.activated.connect(
            lambda: self._refresh_mods()
            if self._combo.currentText() == self._locale["refresh"]
            else None
        )
        self._refresh_mods()

    @property
    def selected(self) -> str:
        return self._combo.currentText()

    def _refresh_mods(self):
        self._combo.clear()
        self._combo.addItem(self._locale["refresh"])
        self._combo.addItem("BackUp")
        self._combo.addItems(self._service.get_applied_mods())
        self._combo.setCurrentIndex(1)

    def reset(self):
        self._combo.setCurrentIndex(1)


class GenModView(ViewBase):
    _edit_mod_name: QLineEdit

    def __init__(self, bin: GuiBin):
        super().__init__(bin)

        self.source_list = SelectSources(bin)
        self.select_base = SelectBaseMod(bin)

        layout = QVBoxLayout()
        layout.addWidget(self.select_base)
        layout.addWidget(self.source_list)
        layout.addLayout(self.init_pack())
        self.setLayout(layout)

    def init_pack(self):
        layout = QHBoxLayout()
        self._edit_mod_name = QLineEdit()
        self._edit_mod_name.setPlaceholderText(
            self._locale["genmods"]["input_mod_name"]
        )
        pack_btn = QPushButton(self._locale["genmods"]["pack"])

        pack_btn.clicked.connect(self._pack)
        layout.addWidget(self._edit_mod_name)
        layout.addWidget(pack_btn)

        return layout

    def _pack(self):
        mod_name = self._edit_mod_name.text().strip()
        selected = self.source_list.selectedItem
        if len(selected) == 0:
            self._bin.show_modal(
                f"{self._locale['item']} {self._locale['notselected']}"
            )
            return
        if mod_name == "":
            self._bin.show_modal("mod name is not defined")
            return
        self._bin.threading(
            self._packJob,
            self._edit_mod_name.text() + " " + self._locale["genmods"]["gen_success"],
            self._locale["genmods"]["pack_failed"],
        )

    def _packJob(self):
        self._service.clear_source()
        if (selected := self.select_base.selected) == "BackUp":
            self._service.reset_base()
        else:
            self._service.select_base_mod(selected)

        mod_name = self._edit_mod_name.text().strip()
        selected = self.source_list.selectedItem

        for source in selected:
            self._bin.process_overlay.desc_text = (
                f"{source} {self._locale['genmods']['preparing']}"
            )
            self._service.prepare_mod_source(source)
        self._bin.process_overlay.desc_text = (
            f"{mod_name} {self._locale['genmods']['packing']}"
        )
        self._service.pack_mod(mod_name)
        self._service.clear_source()
        pass

    def reset(self):
        self.select_base.reset()
        self.source_list.reset()
        self._edit_mod_name.clear()
