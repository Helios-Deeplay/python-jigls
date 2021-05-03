from jeditor.core.graphicedge import JGraphicEdge
from typing import List

from PyQt5.QtCore import QPointF
from .contentwidget import JNodeContent
from .graphicnode import JGraphicNode
from .constants import GREDGE_PATH_BEZIER, GRSCENE_HEIGHT, GRSCENE_WIDTH
from .graphicscene import JiglsGraphicScene


class JSceneManager:
    def __init__(self) -> None:

        self.nodes: List[JGraphicNode] = []
        self.edges = []

        self.initUI()
        self._debug()
        # node.title = "david"

    def initUI(self):
        self._graphicsScene = JiglsGraphicScene()
        self._graphicsScene.SetGraphicsSceneWH(GRSCENE_WIDTH, GRSCENE_HEIGHT)

    @property
    def graphicsScene(self):
        return self._graphicsScene

    def AddNode(self, node: JGraphicNode):
        self.nodes.append(node)

    def AddEdge(self, edge):
        self.edges.append(edge)

    def RemoveNode(self, node: JGraphicNode):
        self.nodes.remove(node)

    def RemoveEdge(self, edge):
        self.nodes.remove(edge)

    def _debug(self):
        node1 = JGraphicNode(inSockets=1, outSockets=1, nodeContent=JNodeContent())
        node2 = JGraphicNode(inSockets=1, outSockets=1, nodeContent=JNodeContent())
        node3 = JGraphicNode(inSockets=1, outSockets=1, nodeContent=JNodeContent())
        # node4 = JGraphicNode(inSockets=1, outSockets=1, nodeContent=JNodeContent())

        node1.setPos(QPointF(-350, -250))
        node2.setPos(QPointF(-75, 0))
        node3.setPos(QPointF(0, 0))

        self.graphicsScene.addItem(node1)
        self.graphicsScene.addItem(node2)
        self.graphicsScene.addItem(node3)
        # self.graphicsScene.addItem(node4)

        edge1 = JGraphicEdge(
            node2.socketManager.GetOutputSocketByIndex(0),
            node3.socketManager.GetInputSocketByIndex(0),
        )
        edge2 = JGraphicEdge(
            node2.socketManager.GetOutputSocketByIndex(0),
            node1.socketManager.GetInputSocketByIndex(0),
            edgePathType=GREDGE_PATH_BEZIER,
        )

        self.graphicsScene.addItem(edge1)
        self.graphicsScene.addItem(edge2)

        # node3 = JGraphicNode(inSockets=2, outSockets=2, nodeContent=JNodeContent())
        # node3.setPos(QPointF(200, -150))
        # self.graphicsScene.addItem(node3)
