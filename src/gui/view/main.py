from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox, QHBoxLayout
from src.service import ModService


class MainView(QWidget):
    def __init__(self, service: ModService):
        super().__init__()
        self.service = service
        self.list_view = None

        self.canvas = None
        self.image_label = None
        self.setLayout(self.content())

    def content(self):
        vbox = QVBoxLayout()
        apply_btn = QPushButton("Apply Mod")
        backup_btn = QPushButton("BackUp")
        backup_btn.clicked.connect(self.service.isolate_original)

        vbox.addWidget(apply_btn)
        vbox.addWidget(backup_btn)
        vbox.addWidget(self.init_restore())
        return vbox

    def init_restore(self):
        link_btn = QPushButton("Link")
        move_btn = QPushButton("Move")
        link_btn.clicked.connect(self.service.restore)

        layout = QHBoxLayout()
        layout.addWidget(link_btn)
        layout.addWidget(move_btn)
        bg = QGroupBox("restore")
        bg.setLayout(layout)
        return bg
