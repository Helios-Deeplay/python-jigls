# from jiglsgui.graphicedge import JigleGraphicEdge
from jiglsgui.graphicedge import JigleGraphicEdge, JigleGraphicEdgeBezier
from jiglsgui.graphicsnode import JigleGraphicNode
from jiglsgui.scene import JigleScene
from jiglsgui.graphicview import JiglsGraphicView
from PyQt5 import QtWidgets, QtCore


class NodeEditorWindow(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Node Editor")
        self.setGeometry(200, 200, 800, 600)
        self.layout = QtWidgets.QVBoxLayout()  # type:ignore
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # * graphics scene
        self.scene = JigleScene()
        # self.grScene = self.scene.grScene

        # * graphic view here
        self.view = JiglsGraphicView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.AddNode()
        self.AddEdge()

    def AddNode(self):
        node1 = JigleGraphicNode(title="web element 1")
        node2 = JigleGraphicNode(title="web element 2")
        edge1 = JigleGraphicEdgeBezier("edge1")

        self.scene.grScene.addItem(node1)
        self.scene.grScene.addItem(node2)
        self.scene.grScene.addItem(edge1)

        node1.setPos(0, 250)
        node2.setPos(75, 0)

        # self.scene.addNode(node1)
        # self.scene.addNode(node2)

    def AddEdge(self):
        pass

        # self.AddDebugContent()

    # def AddDebugContent(self):

    #     qBrush = QBrush(QtCore.Qt.green)
    #     qPen = QPen(QtCore.Qt.black)
    #     qPen.setWidth(2)

    #     rect = self.scene.grScene.addRect(
    #         -100,
    #         -100,
    #         80,
    #         100,
    #         qPen,
    #         qBrush,
    #     )
    #     rect.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)

    #     text = self.grScene.addText(
    #         "this is my awesom text", QFont("Ubuntu")
    #     )
    #     text.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
    #     text.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
