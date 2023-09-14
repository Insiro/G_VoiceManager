from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QWidget
from src.gui.view import ModView, MainView, ConfigView
from src.gui.view.process_overlay import ProcessOverlay
from src.service import ModService
from qt_material import apply_stylesheet


class MyApp(QWidget):
    @property
    def overlay(self):
        return self.__overlay

    @property
    def current(self):
        return self.side_bar.current

    def __init__(self, service: ModService):
        super().__init__()
        self.service = service
        self.__overlay = ProcessOverlay(self)
        layout = QVBoxLayout()
        layout.addWidget(self.init_header())
        layout.addWidget(self.init_tab())
        self.setLayout(layout)
        self.setWindowTitle("Genshin Voice Manager")
        self.show()

    def init_header(self):
        return QtWidgets.QLabel("header area")

    def init_tab(self):
        subPage = QWidget()
        tab = QTabWidget(subPage)
        tab.addTab(MainView(self.service, self.show_process), "Home")
        tab.addTab(ModView(self.service, self.show_process), "Mod Manage")
        tab.addTab(ConfigView(self.service), "Config")
        subPage.setMinimumSize(tab.sizeHint())
        return subPage


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
