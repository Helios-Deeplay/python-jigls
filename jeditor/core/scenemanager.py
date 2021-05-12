import json
import logging
from typing import Dict, List, Optional

from jeditor.logger import logger
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QUndoStack
from .constants import (
    GREDGE_PATH_BEZIER,
    GRSCENE_HEIGHT,
    GRSCENE_WIDTH,
    GRSOCKET_TYPE_INPUT,
    GRSOCKET_TYPE_OUTPUT,
)
from .graphicedge import JGraphicEdge
from .graphicnode import JGraphicNode
from .graphicscene import JGraphicScene
from .graphicsocket import JGraphicSocket
from .nodefactory import JNodeFactory

logger = logging.getLogger(__name__)


class JSceneManager(QtCore.QObject):
    def __init__(self) -> None:
        super().__init__(parent=None)

        self._graphicsScene = JGraphicScene()
        self._nodeFactory = JNodeFactory()
        self._undoStack = QUndoStack(self._graphicsScene)
        self._graphicsScene.SetGraphicsSceneWH(GRSCENE_WIDTH, GRSCENE_HEIGHT)

        self._debug()

    @property
    def graphicsScene(self) -> JGraphicScene:
        return self._graphicsScene

    @property
    def undoStack(self) -> QUndoStack:
        return self._undoStack

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
        logger.info("serializing")
        node: List[Dict] = []
        edge: List[Dict] = []
        for item in self._graphicsScene.items():
            if isinstance(item, JGraphicNode):
                node.append(item.Serialize())
            if isinstance(item, JGraphicEdge):
                edge.append(item.Serialize())
        return {"nodes": node, "edges": edge}

    def Deserialize(self, data: Dict):
        logger.info("deserializing")
        self._graphicsScene.clear()
        for node in data["nodes"]:
            instanceNode = JGraphicNode.Deserialize(node)
            self._graphicsScene.addItem(instanceNode)

        for edge in data["edges"]:
            edgeId = edge["edgeId"]
            sourceSocketId = edge["sourceSocketId"]
            desitnationSocketId = edge["desitnationSocketId"]

            sourceSocket: Optional[JGraphicSocket] = None
            destinationSocket: Optional[JGraphicSocket] = None

            for socket in list(
                filter(
                    lambda socket_: isinstance(socket_, JGraphicSocket),
                    self._graphicsScene.items(),
                )
            ):
                assert isinstance(socket, JGraphicSocket)
                if socket.socketId == sourceSocketId:
                    sourceSocket = socket
                elif socket.socketId == desitnationSocketId:
                    destinationSocket = socket

            assert sourceSocket, logger.error("source socket not found")
            assert destinationSocket, logger.error("destination socket not found")

            instanceEdge = JGraphicEdge.Deserialize(
                edgeId, sourceSocket, destinationSocket
            )

            self._graphicsScene.addItem(instanceEdge)

    def SaveToFile(self):
        logger.debug("saving to file")
        with open("graph.json", "w") as file:
            json.dump(obj=self.Serialize(), fp=file)

    def LoadFromFile(self) -> Dict:
        logger.debug("loading from file")
        with open("graph.json", "r") as file:
            data = json.load(file)
            return data

    def AddNode(self):
        pass

    def RemoveNode(self):
        pass

    def AddEdge(self):
        pass

    def RemoveEdge(self):
        pass
