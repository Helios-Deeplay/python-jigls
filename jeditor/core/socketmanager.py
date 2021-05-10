import logging
import typing
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union
import uuid

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtCore
from jeditor.core import graphicnode
from jeditor.logger import logger
from PyQt5.QtCore import QPointF

from .constants import (
    GRNODE_EDGE_SIZE,
    GRNODE_NODE_HEIGHT,
    GRNODE_NODE_WIDHT,
    GRNODE_TITLE_HEIGHT,
    GRNODE_TITLE_PADDING,
    GRSOCKET_POS_LEFT_BOTTOM,
    GRSOCKET_POS_RIGHT_BOTTOM,
    GRSOCKET_POS_RIGHT_TOP,
    GRSOCKET_SPACING,
    GRSOCKET_TYPE_INPUT,
    GRSOCKET_TYPE_OUTPUT,
)
from .graphicsocket import JGraphicSocket

if TYPE_CHECKING:
    from .graphicnode import JGraphicNode


logger = logging.getLogger(__name__)


class JNodeSocketManager:
    def __init__(self, parent: QGraphicsItem, nodeId: str) -> None:

        self._parent = parent
        self._nodeId = nodeId
        self._inSocketsList: List[JGraphicSocket] = []
        self._outSocketsList: List[JGraphicSocket] = []
        self._socketCount: int = 0

    @property
    def inSocketCount(self) -> int:
        return len(self._inSocketsList)

    @property
    def outSocketCount(self) -> int:
        return len(self._outSocketsList)

    @property
    def inSocketsList(self) -> List[JGraphicSocket]:
        return self._inSocketsList

    @property
    def outSocketsList(self) -> List[JGraphicSocket]:
        return self._outSocketsList

    @property
    def socketList(self) -> List[JGraphicSocket]:
        return self._inSocketsList + self._outSocketsList

    @property
    def socketCount(self) -> int:
        return self._socketCount

    def GetSocketByIndex(self, index: int) -> JGraphicSocket:
        return list(self._inSocketsList + self._outSocketsList)[index]

    def GetSocketById(self, socketId: str) -> Optional[JGraphicSocket]:
        socketL = list(
            filter(lambda socket: socket.socketId == socketId, self.socketList)
        )
        if socketL is None:
            return None
        else:
            return socketL[0]

    def AddSocket(
        self,
        socketId: Optional[str],
        type: int,
        multiConnection: bool = True,
    ) -> int:

        if socketId is None:
            socketId = uuid.uuid4().hex

        if type == GRSOCKET_TYPE_INPUT:
            return self.AddInputSocket(
                socketId=socketId, multiConnection=multiConnection
            )
        elif type == GRSOCKET_TYPE_OUTPUT:
            return self.AddOutputSocket(
                socketId=socketId, multiConnection=multiConnection
            )
        else:
            return -1

    def AddInputSocket(
        self,
        socketId: str = None,
        multiConnection: bool = True,
        position=GRSOCKET_POS_LEFT_BOTTOM,
    ) -> int:

        if socketId is None:
            socketId = uuid.uuid4().hex

        socket = JGraphicSocket(
            parent=self._parent,
            nodeId=self._nodeId,
            socketId=socketId,
            index=self._socketCount,
            socketType=GRSOCKET_TYPE_INPUT,
            multiConnection=multiConnection,
        )

        socket.setPos(self._CalculateSocketPos(len(self._inSocketsList), position))

        self._inSocketsList.append(socket)
        self._socketCount += 1
        return self._socketCount - 1

    def AddOutputSocket(
        self,
        socketId: str,
        multiConnection: bool = True,
        position=GRSOCKET_POS_RIGHT_TOP,
    ) -> int:

        socket = JGraphicSocket(
            parent=self._parent,
            nodeId=self._nodeId,
            socketId=socketId,
            index=self._socketCount,
            socketType=GRSOCKET_TYPE_OUTPUT,
            multiConnection=multiConnection,
        )

        socket.setPos(self._CalculateSocketPos(len(self._outSocketsList), position))

        self._outSocketsList.append(socket)
        self._socketCount += 1
        return self._socketCount - 1

    def _CalculateSocketPos(self, index: int, position: int) -> QPointF:

        # * left posiition
        x = 0

        # * right posiition
        if position in [GRSOCKET_POS_RIGHT_BOTTOM, GRSOCKET_POS_RIGHT_TOP]:
            x = GRNODE_NODE_WIDHT

        # * top position
        vertPadding = GRNODE_TITLE_HEIGHT + GRNODE_TITLE_PADDING + GRNODE_EDGE_SIZE
        y = vertPadding + index * GRSOCKET_SPACING

        # * bottom position
        if position in [GRSOCKET_POS_LEFT_BOTTOM, GRSOCKET_POS_RIGHT_BOTTOM]:
            y = GRNODE_NODE_HEIGHT - vertPadding - index * GRSOCKET_SPACING

        return QPointF(x, y)

    def Serialize(self):
        res: Dict[Any, Any] = {
            "socketCount": self._socketCount,
        }
        socD: Dict[int, Dict[str, Union[int, str]]] = {}
        for socket in self.socketList:
            socD.update(
                {
                    socket.index: {
                        "socketId": socket.socketId,
                        "socketType": socket.socketType,
                        "multiConnection": socket.multiConnection,
                    },
                }
            )
        res.update({"socketInfo": socD})
        return res