from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import QSize, Qt, QThread, QTimer
from PyQt6.QtGui import QMovie, QPalette, QColor


class ProcessOverlay(QWidget):
    def __init__(
        self, parent: QWidget, desc_text: str = "", dot_animation: bool = True
    ):
        super().__init__(parent)
        self.__parent = parent
        parent.installEventFilter(self)
        self.dot_animation = dot_animation
        self.desc_text = desc_text
        self.__initUi(desc_text)

    def __initUi(self, description_text):
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.__loading_mv = QMovie("./resources/loading.gif")
        self.__loading_mv.setScaledSize(QSize(45, 45))
        mv_label = QLabel(self.__parent)
        mv_label.setMovie(self.__loading_mv)
        mv_label.setStyleSheet("QLabel { background: transparent; }")
        mv_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        )

        self.__desc_label = QLabel(description_text)
        self.__desc_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        )

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(mv_label)
        layout.addWidget(self.__desc_label)
        self.setLayout(layout)
        self.setMinimumSize(self.__parent.width(), self.__parent.height())
        self.setVisible(False)
        if self.dot_animation:
            self.__tick = 0
            self.__timer = QTimer(self)
            self.__timer.timeout.connect(self._ticking)
            self.__timer.singleShot(0, self._ticking)

    def _ticking(self):
        self.__tick = (self.__tick) % 3 + 1
        self.__desc_label.setText(self.desc_text + "." * (self.__tick))

    def start(self):
        self.setVisible(True)
        self.__loading_mv.start()
        self.raise_()

        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.75))
        if self.dot_animation:
            self.__timer.start(500)
        self.__parent.setEnabled(False)

    def stop(self):
        self.__loading_mv.stop()
        self.lower()
        self.__timer.stop()
        self.setVisible(False)
        self.__parent.setEnabled(True)

    def paintEvent(self, e):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        return super().paintEvent(e)

    def eventFilter(self, obj, e):
        if isinstance(obj, QWidget):
            if e.type() == 14:
                self.setFixedSize(e.size())
        return super().eventFilter(obj, e)
