from PyQt5 import QtWidgets
from typing import Optional
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QGraphicsTextItem,
    QLabel,
    QStyleOptionGraphicsItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class JNodeContent(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()  # type:ignore
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        wdg_label = QLabel("Some Title")
        wdg_label.setObjectName("1")
        wdg_label.setHidden(True)
        self.layout.addWidget(wdg_label)

        textEdit = QTextEdit("foo")
        textEdit.setObjectName("2")
        textEdit.setHidden(True)

        self.layout.addWidget(textEdit)
