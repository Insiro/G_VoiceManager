from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QWidget
from src.gui.bin import Bin
from src.gui.view import ModView, MainView, ConfigView


from src.service import ModService


class MyApp(QWidget):
    @property
    def overlay(self):
        return self.__overlay

    @property
    def current(self):
        return self.side_bar.current

    def __init__(self, service: ModService):
        super().__init__()
        self.__bin = Bin(self, service)
        self.__locale = self.__bin.locale
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
        tab.addTab(MainView(self.__bin), self.__locale["tab"]["home"])
        tab.addTab(ModView(self.__bin), self.__locale["tab"]["gen_mod"])
        tab.addTab(ConfigView(self.__bin), self.__locale["tab"]["config"])
        tab.currentChanged.connect(lambda x: tab.currentWidget().reset())
        subPage.setMinimumSize(tab.sizeHint())
        return subPage


def showDialog(base_dir):
    filename, _ = QtWidgets.QFileDialog.getExistingDirectory(
        None, "Open folder", base_dir
    )


import sys
from qt_material import apply_stylesheet


def start_gui(argv, service: ModService):
    app = QtWidgets.QApplication(argv)
    apply_stylesheet(app, theme="light_blue.xml")
    ex = MyApp(service)
    sys.exit(app.exec())
