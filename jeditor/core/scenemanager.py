from .graphicedgepath import (
    JGraphicEdgeBezier,
    JGraphicEdgeDirect,
    JGraphicEdgeSquare,
)
from typing import List

from PyQt5.QtCore import QPointF
from .contentwidget import JNodeContent
from .graphicnode import JGraphicNode
from .constants import GRSCENE_HEIGHT, GRSCENE_WIDTH
from .graphicscene import JiglsGraphicScene


class JSceneManager:
    def __init__(self) -> None:

        self.nodes: List[JGraphicNode] = []
        self.edges = []

        self.initUI()
        self._debug()
        # node.title = "david"

    def initUI(self):
        self._graphicScene = JiglsGraphicScene()
        self._graphicScene.SetGraphicsSceneWH(GRSCENE_WIDTH, GRSCENE_HEIGHT)

    @property
    def graphicsScene(self):
        return self._graphicScene

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

        node1.setPos(QPointF(-350, -250))
        node2.setPos(QPointF(-75, 0))

        self.graphicsScene.addItem(node1)
        self.graphicsScene.addItem(node2)

        for i in range(100):
            self.graphicsScene.addItem(
                JGraphicNode(inSockets=1, outSockets=1, nodeContent=JNodeContent())
            )

        # edge1 = JGraphicEdgeDirect(
        #     node1.socketManager.GetOutputSocketByIndex(0),
        #     node2.socketManager.GetInputSocketByIndex(0),
        # )
        edge2 = JGraphicEdgeSquare(
            node2.socketManager.GetOutputSocketByIndex(0),
            node1.socketManager.GetInputSocketByIndex(0),
        )

        # self.graphicsScene.addItem(edge1)
        self.graphicsScene.addItem(edge2)

        # node3 = JGraphicNode(inSockets=2, outSockets=2, nodeContent=JNodeContent())
        # node3.setPos(QPointF(200, -150))
        # self.graphicsScene.addItem(node3)
