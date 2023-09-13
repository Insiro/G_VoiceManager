from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QWidget
from src.gui.view import ModView, MainView, ConfigView
from src.service import ModService
from qt_material import apply_stylesheet


class MyApp(QWidget):
    def __init__(self, service: ModService):
        super().__init__()
        self.service = service
        self._layout = QVBoxLayout()

        self.init_ui()

    @property
    def current(self):
        return self.side_bar.current

    def init_header(self):
        wid = QtWidgets.QLabel()
        wid.setText("header area")

        return wid

    def init_tab(self):
        subPage = QWidget()
        tab = QTabWidget(subPage)
        tab.addTab(MainView(self.service), "Home")
        tab.addTab(ModView(self.service), "Mod Manage")
        tab.addTab(ConfigView(self.service), "Config")
        subPage.setMinimumSize(tab.sizeHint())
        return subPage

    def init_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self.init_header())
        self._layout.addWidget(self.init_tab())
        self.setWindowTitle("Genshin Voice Manager")
        self.show()


def showDialog(base_dir):
    filename, _ = QtWidgets.QFileDialog.getExistingDirectory(
        None, "Open folder", base_dir
    )


import sys


def start_gui(argv, service):
    app = QtWidgets.QApplication(argv)
    apply_stylesheet(app, theme="light_blue.xml")
    ex = MyApp(service)
    sys.exit(app.exec())
