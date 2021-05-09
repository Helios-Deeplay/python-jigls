from jeditor.core.nodefactory import JNodeFactory
from jeditor.core.graphicedge import JGraphicEdge
from typing import Dict, List

from PyQt5.QtCore import QPointF
from .contentwidget import JNodeContent
from .graphicnode import JGraphicNode
from .constants import (
    GREDGE_PATH_BEZIER,
    GRSCENE_HEIGHT,
    GRSCENE_WIDTH,
    GRSOCKET_TYPE_INPUT,
    GRSOCKET_TYPE_OUTPUT,
)
from .graphicscene import JGraphicScene
from pprint import pprint
import json


class JSceneManager:
    def __init__(self) -> None:

        self.initUI()
        self._debug()

    def initUI(self):
        self._graphicsScene = JGraphicScene()
        self._nodeFactory = JNodeFactory()
        self._graphicsScene.SetGraphicsSceneWH(GRSCENE_WIDTH, GRSCENE_HEIGHT)

    @property
    def graphicsScene(self):
        return self._graphicsScene

    def _debug(self):
        node1 = self._nodeFactory.CreateNode(None, False, False)
        node2 = self._nodeFactory.CreateNode(None, True, True)
        node3 = self._nodeFactory.CreateNode(None, True, False)
        # node4 = JGraphicNode(inSockets=1, outSockets=1, nodeContent=JNodeContent())

        node1.setPos(QPointF(-350, -250))
        node2.setPos(QPointF(-75, 0))
        node3.setPos(QPointF(0, 0))

        self.graphicsScene.addItem(node1)
        self.graphicsScene.addItem(node2)
        self.graphicsScene.addItem(node3)

    def Serialize(self) -> Dict:
        node: List[Dict] = []
        edge: List[Dict] = []
        for item in self._graphicsScene.items():
            if isinstance(item, JGraphicNode):
                node.append(item.Serialize())
            if isinstance(item, JGraphicEdge):
                edge.append(item.Serialize())
        return {"nodes": node, "edges": edge}

    def Deserialize(self, data: Dict):
        self._graphicsScene.clear()
        for node in data["nodes"]:
            instanceNode = JGraphicNode.Deserialize(node)
            self._graphicsScene.addItem(instanceNode)

        for edge in data["edges"]:
            nodes = list(
                filter(
                    lambda x: x.nodeIdentifier  # type:ignore
                    in [edge["sourceNodePID"], edge["destinationNodePID"]],
                    list(
                        filter(
                            lambda item: isinstance(item, JGraphicNode),
                            self._graphicsScene.items(),
                        )
                    ),
                )
            )
            assert len(nodes) == 2
            startSocket = None
            destinationSocket = None
            for node in nodes:
                assert isinstance(node, JGraphicNode)
                if node.nodeIdentifier == edge["sourceNodePID"]:
                    startSocket = node.socketManager.GetSocketByIndex(
                        edge["sourceNodeIndex"]
                    )
                if node.nodeIdentifier == edge["destinationNodePID"]:
                    destinationSocket = node.socketManager.GetSocketByIndex(
                        edge["destinationNodeIndex"]
                    )

            self._graphicsScene.addItem(
                JGraphicEdge.Deserialize(
                    identifier=edge["identifier"],
                    startSocket=startSocket,
                    destinationSocket=destinationSocket,
                )
            )

    def SaveToFile(self):
        with open("graph.json", "w") as file:
            json.dump(obj=self.Serialize(), fp=file)

    def LoadFromFile(self) -> Dict:
        with open("graph.json", "r") as file:
            data = json.load(file)
            return data
