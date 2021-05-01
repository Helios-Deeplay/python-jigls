from typing import List
from .contentwidget import JNodeContent
from .graphicnode import JGraphicNode
from .constants import GRSCENE_HEIGHT, GRSCENE_WIDTH
from .graphicscene import JiglsGraphicScene


class JSceneManager:
    def __init__(self) -> None:

        self.nodes: List[JGraphicNode] = []
        self.edges = []

        self.initUI()

        node = JGraphicNode()  # nodeContent=JNodeContent())
        self.graphicsScene.addItem(node)
        node.title = "david"

    def initUI(self):
        self._grScene = JiglsGraphicScene()
        self._grScene.SetGrSceneWH(GRSCENE_WIDTH, GRSCENE_HEIGHT)

    @property
    def graphicsScene(self):
        return self._grScene

    def AddNode(self, node: JGraphicNode):
        self.nodes.append(node)

    def AddEdge(self, edge):
        self.edges.append(edge)

    def RemoveNode(self, node: JGraphicNode):
        self.nodes.remove(node)

    def RemoveEdge(self, edge):
        self.nodes.remove(edge)