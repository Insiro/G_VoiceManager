from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QComboBox,
)
from src.service import ModService


class MainView(QWidget):
    mod_ComboBox: QComboBox
    restore_combo: QComboBox

    def __init__(self, service: ModService):
        super().__init__()
        self.service = service
        self.setLayout(self.init_content())

    def init_content(self):
        vbox = QVBoxLayout()
        backup_btn = QPushButton("BackUp")
        backup_btn.clicked.connect(self.service.isolate_original)

        vbox.addWidget(self.init_mod_group())
        vbox.addWidget(self.init_restore_group())
        vbox.addWidget(backup_btn)
        return vbox

    def init_mod_group(self):
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply)
        self.mod_ComboBox = QComboBox()
        self.load_mods()
        self.mod_ComboBox.setPlaceholderText("--Select Mod--")
        self.mod_ComboBox.setCurrentIndex(-1)

        layout = QHBoxLayout()
        layout.addWidget(self.mod_ComboBox)
        layout.addWidget(apply_btn)
        bg = QGroupBox("Apply Mod")
        bg.setLayout(layout)

        return bg

    def init_restore_group(self):
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

    def restore(self):
        selected = self.restore_combo.currentText()
        self.service.restore(selected == "link")

    def apply(self):
        idx = self.mod_ComboBox.currentIndex()
        if idx == 0:
            self.load_mods()
            return
        mod_name = self.mod_ComboBox.currentText()
        print(mod_name)
        # self.service.apply(mod_name)

    def load_mods(self):
        self.mod_ComboBox.clear()
        self.mod_ComboBox.addItem("refresh list")
        mod_list = self.service.get_applied_mods()
        self.mod_ComboBox.addItems(mod_list)
