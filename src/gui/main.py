import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from qt_material import apply_stylesheet

from .alert import Alert
from .bin import Config, GuiBin
from .g_path_fix import GPathFix
from .view import ConfigView, GenModView, MainView, ModView


class MyApp(QWidget):
    @property
    def overlay(self):
        return self.__overlay

    @property
    def current(self):
        return self.side_bar.current

    def __init__(self, bin: GuiBin):
        super().__init__()
        self.__bin = bin
        bin.connectApp(self)
        self.__locale = self.__bin.locale
        layout = QVBoxLayout()
        layout.addWidget(self.init_tab())
        self.setLayout(layout)
        self.setWindowTitle("Genshin Voice Manager")
        self.setWindowIcon(QIcon(".\\assets\icon.ico"))
        self.show()

    def init_tab(self):
        subPage = QWidget()
        tab = QTabWidget(subPage)
        tab.addTab(MainView(self.__bin), self.__locale["tab"]["home"])
        tab.addTab(ModView(self.__bin), self.__locale["tab"]["mod"])
        tab.addTab(GenModView(self.__bin), self.__locale["tab"]["gen_mod"])
        tab.addTab(ConfigView(self.__bin), self.__locale["tab"]["config"])
        tab.currentChanged.connect(lambda: tab.currentWidget().reset())
        subPage.setMinimumSize(tab.sizeHint())
        return subPage


def start(argv, config: Config):
    bin = GuiBin(config)
    if not config.hide:
        alertApp = QtWidgets.QApplication(argv)
        apply_stylesheet(alertApp, theme=config.theme, invert_secondary=True)
        alert = Alert(bin)
        alert.show()
        alertApp.exec()
        if not alert.agree:
            exit()
    if not bin.service.valiDateGenshinDir:
        gpfApp = QtWidgets.QApplication(argv)
        apply_stylesheet(gpfApp, theme=config.theme, invert_secondary=True)
        ex = GPathFix(bin)
        ex.show()
        gpfApp.exec()
        if not ex.passed:
            exit()

    bin = GuiBin(config)
    mainApp = QtWidgets.QApplication(argv)
    apply_stylesheet(mainApp, theme=config.theme, invert_secondary=True)
    try:
        ex = MyApp(bin)
        sys.exit(mainApp.exec())
    except Exception as e:
        import traceback

        bin.logger.error(traceback.format_exc())
