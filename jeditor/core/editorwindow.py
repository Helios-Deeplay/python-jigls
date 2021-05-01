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
        return self._sceneManager._graphicScene

    @property
    def graphicView(self) -> QtWidgets.QGraphicsView:
        return self._graphicsView
