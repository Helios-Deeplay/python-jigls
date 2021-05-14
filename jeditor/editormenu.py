from typing import Callable, Optional
from jeditor.core.scenemanager import JSceneManager
from jeditor.stylesheet import STYLE_QMENUBAR
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction

# https://zetcode.com/gui/pyqt5/menustoolbars/


def CreateAction(
    parent: QtWidgets.QMenuBar,
    name: str,
    shortcut: str,
    tooltip: str,
    callback: Optional[Callable] = None,
) -> QAction:

    action = QAction(name, parent=parent)
    action.setShortcut(shortcut)
    action.setToolTip(tooltip)
    action.triggered.connect(callback)
    return action


class JMenuBar(QtWidgets.QMenuBar):
    def __init__(self, editorWidget: JSceneManager):
        super().__init__(parent=None)
        self._editorWidget = editorWidget
        self.setStyleSheet(STYLE_QMENUBAR)

        self._SetupMenu()

    def _SetupMenu(self):

        fileMenu = self.addMenu("&File")
        editMenu = self.addMenu("&Edit")
        graphMenu = self.addMenu("&Graph")
        helpMenu = self.addMenu("&Help")

        fileMenu.addAction(
            CreateAction(
                self, "&Open", "Ctrl+1", "Open new graph model", self.OpenModel
            )
        )

    def OpenModel(self):
        print("dis is a test")
