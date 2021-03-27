from typing import List
from jiglsgui.graphicsnode import JigleGraphicNode
from jiglsgui.graphicscene import JiglsGraphicScene


class JigleScene:
    """Class representing NodeEditor's `Scene`"""

    def __init__(self):
        super().__init__()
        self.nodes: List[JigleGraphicNode] = []
        self.edges = []

        self.sceneWidth = 64000
        self.sceneHeight = 64000

        self.initUI()

    def initUI(self):
        self.grScene = JiglsGraphicScene(self)
        self.grScene.SetGrScene(self.sceneWidth, self.sceneHeight)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)