from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QListWidgetItem,
    QAbstractItemView,
    QLineEdit,
)
from src.gui.bin import Bin
from .view_base import ViewBase


class SelectSources(QGroupBox):
    @property
    def selectedItem(self) -> list[str]:
        return [item.text() for item in self._source_list.selectedItems()]

    def __init__(self, bin: Bin) -> None:
        super().__init__()
        self._locale = bin.locale
        self.setTitle(self._locale["mods"]["source_select"])
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


class SelectBaseMod(QHBoxLayout):
    def __init__(self, bin: Bin):
        super().__init__()
        self._locale = bin.locale
        self._service = bin.service
        self._base_combo = QComboBox()
        self._base_combo.activated.connect(
            lambda: self._refresh_mods()
            if self._base_combo.currentText() == self._locale["refresh"]
            else None
        )
        self._refresh_mods()

        self.addWidget(QLabel(self._locale["mods"]["mod_base"]))
        self.addWidget(self._base_combo)

    @property
    def selected(self) -> str:
        return self._base_combo.currentText()

    def _refresh_mods(self):
        self._base_combo.clear()
        self._base_combo.addItem(self._locale["refresh"])
        self._base_combo.addItem("BackUp")
        self._base_combo.addItems(self._service.get_applied_mods())
        self._base_combo.setCurrentIndex(1)

    def reset(self):
        self._base_combo.setCurrentIndex(1)


class ModView(ViewBase):
    _edit_mod_name: QLineEdit

    def __init__(self, bin: Bin):
        super().__init__(bin)

        self.source_list = SelectSources(bin)
        self.select_base = SelectBaseMod(bin)

        layout = QVBoxLayout()
        layout.addLayout(self.select_base)
        layout.addWidget(self.source_list)
        layout.addLayout(self.init_pack())
        self.setLayout(layout)

    def init_pack(self):
        layout = QHBoxLayout()
        self._edit_mod_name = QLineEdit()
        self._edit_mod_name.setPlaceholderText(self._locale["mods"]["input_mod_name"])
        pack_btn = QPushButton(self._locale["mods"]["pack"])

        pack_btn.clicked.connect(
            lambda: self.bin.threading(
                self._pack,
                self._edit_mod_name.text() + " " + self._locale["mods"]["gen_success"],
                self._locale["mods"]["pack_failed"],
            )
        )
        layout.addWidget(self._edit_mod_name)
        layout.addWidget(pack_btn)

        return layout

    def _pack(self):
        self._service.clear_source()
        if (selected := self.select_base.selected) == "BackUp":
            self._service.reset_base()
        else:
            self._service.select_base_mod(selected)
        for source in self.source_list.selectedItem:
            self.bin.process_overlay.desc_text = (
                f"{source} {self._locale['mods']['preparing']}"
            )
            self._service.prepare_mod_source(source)
        mod_name = self._edit_mod_name.text()
        self.bin.process_overlay.desc_text = (
            f"{mod_name} {self._locale['mods']['packing']}"
        )
        self._service.pack_mod(mod_name)
        self._service.clear_source()
        pass

    def reset(self):
        self.select_base.reset()
        self.source_list.reset()
        self._edit_mod_name.clear()
