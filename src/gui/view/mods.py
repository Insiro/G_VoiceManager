from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QLabel,
    QListWidgetItem,
    QAbstractItemView,
    QLineEdit,
)
from src.gui.bin import Bin


class SelectSources(QGroupBox):
    @property
    def selectedItem(self) -> list[str]:
        return [item.text() for item in self._source_list.selectedItems()]

    def __init__(self, bin: Bin) -> None:
        super().__init__()
        self.setTitle("Select Mod Sources")
        self._service = bin.service

        self._source_list = QListWidget()
        self._source_list.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self._source_list.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_mod_list)

        layout = QVBoxLayout()
        layout.addWidget(self._source_list)
        layout.addWidget(refresh_btn)
        self._refresh_mod_list()
        self.setLayout(layout)

    def _refresh_mod_list(self):
        self.mod_sources = self._service.get_mod_sources()
        self._source_list.clear()

        self._source_list.addItem("1")
        self._source_list.addItem("1")
        self._source_list.addItem("1")
        for source in self.mod_sources:
            item = QListWidgetItem(source)
            self._source_list.addItem(item)

    def reset(self):
        self._source_list.reset()


class SelectBaseMod(QHBoxLayout):
    def __init__(self, bin: Bin):
        super().__init__()
        self._service = bin.service
        self._base_combo = QComboBox()
        self._base_combo.activated.connect(
            lambda: self._refresh_mods()
            if self._base_combo.currentText() == "Refresh"
            else None
        )
        self._refresh_mods()

        self.addWidget(QLabel("Mod Base"))
        self.addWidget(self._base_combo)

    @property
    def selected(self) -> str:
        return self._base_combo.currentText()

    def _refresh_mods(self):
        self._base_combo.clear()
        self._base_combo.addItem("Refresh")
        self._base_combo.addItem("BackUp")
        self._base_combo.addItems(self._service.get_applied_mods())
        self._base_combo.setCurrentIndex(1)

    def reset(self):
        self._base_combo.setCurrentIndex(1)


class ModView(QWidget):
    _edit_mod_name: QLineEdit

    def __init__(self, bin: Bin):
        super().__init__()
        self.bin = bin
        self._service = bin.service

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
        self._edit_mod_name.setPlaceholderText("input new mod name")
        pack_btn = QPushButton("Pack Mod")
        pack_btn.clicked.connect(self._pack)
        layout.addWidget(self._edit_mod_name)
        layout.addWidget(pack_btn)

        return layout

    def _pack(self):
        return
        self._service.clear_source()
        if (selected := self.select_base.selected) == "BackUp":
            self._service.reset_base()
        else:
            self._service.select_base_mod(selected)
        for source in self.source_list.selectedItem:
            self._service.prepare_mod_source(source)
        self._pack()
        self._service.clear_source()
        pass

    def reset(self):
        self.select_base.reset()
        self.source_list.reset()
        self._edit_mod_name.clear()
