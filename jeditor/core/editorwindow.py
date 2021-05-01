# from gui.graphicedge import JigleGraphicEdge
from .graphicnode import JGraphicNode
from .scenemanager import JSceneManager
from .graphicview import JGraphicView
from PyQt5.QtGui import QBrush, QFont, QPen
from .graphicscene import JiglsGraphicScene

from PyQt5 import QtWidgets, QtCore


class JEditorWindow(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.setWindowTitle("JIGLS Editor")
        self.setGeometry(200, 200, 800, 600)

        # * set layout
        self.layout_ = QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_)

        # * graphics scene
        self._sceneManager = JSceneManager()

        # * graphic view here
        self._graphicsView = JGraphicView(self.graphicsScene, self)
        self.layout_.addWidget(self._graphicsView)

    @property
    def graphicsScene(self) -> QtWidgets.QGraphicsScene:
        return self._sceneManager._grScene

    @property
    def graphicView(self) -> QtWidgets.QGraphicsView:
        return self._graphicsView


def AddDebugContent(self):

    qBrush = QBrush(QtCore.Qt.green)
    qPen = QPen(QtCore.Qt.black)
    qPen.setWidth(2)

    rect = self.graphicsScene.addRect(
        -100,
        -100,
        80,
        100,
        qPen,
        qBrush,
    )
    rect.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)

    text = self.graphicsScene.addText(
        "this is my awesom text", QFont("Ubuntu")
    )
    text.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
    text.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
