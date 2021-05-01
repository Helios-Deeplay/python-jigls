import typing
from jeditor.core import graphicnode
from typing import List, Tuple

from PyQt5.QtCore import QPointF

from .constants import (
    GRSOCKET_POS_LEFT_BOTTOM,
    GRSOCKET_POS_RIGHT_BOTTOM,
    GRSOCKET_POS_RIGHT_TOP,
    GRSOCKET_SPACING,
    GRSOCKET_TYPE_INPUT,
    GRSOCKET_TYPE_OUTPUT,
)
from .graphicsocket import JGraphicSocket

try:
    from .graphicnode import JGraphicNode
except:
    from PyQt5.QtWidgets import QGraphicsItem


class JSocketManager:
    def __init__(self, parent, inSockets: int = 1, outSockets: int = 1) -> None:

        assert inSockets >= 1
        assert outSockets >= 1

        self._parentNode: JGraphicNode = parent

        self._inSocketsList: List[JGraphicSocket] = []
        self._outSocketsList: List[JGraphicSocket] = []

        self._InitVariables()

        for _ in range(inSockets):
            self.AddInputSocket()
        for _ in range(outSockets):
            self.AddOutputSocket()

    def _InitVariables(self):
        self._socketSpacing = GRSOCKET_SPACING
        self._socketCount: int = 0

    @property
    def socketCount(self):
        return self._socketCount

    @property
    def inSocketCount(self):
        return len(self._inSocketsList)

    @property
    def outSocketCount(self):
        return len(self._outSocketsList)

    def GetInputSocketByIndex(self, index: int) -> JGraphicSocket:
        return self._inSocketsList[index]

    def GetOutputSocketByIndex(self, index: int) -> JGraphicSocket:
        return self._outSocketsList[index]

    def GetInputSocketPosByIndex(self, index: int) -> QPointF:
        return self.GetInputSocketByIndex(index).pos()

    def GetOutputSocketPosByIndex(self, index: int) -> QPointF:
        return self.GetOutputSocketByIndex(index).pos()

    def AddInputSocket(self, position=GRSOCKET_POS_LEFT_BOTTOM) -> int:

        socket = JGraphicSocket(
            self._parentNode, self._socketCount, GRSOCKET_TYPE_INPUT
        )

        socket.setPos(self.CalcSocketPos(len(self._inSocketsList), position))

        self._inSocketsList.append(socket)
        self._socketCount += 1
        return self._socketCount - 1

    def AddOutputSocket(self, position=GRSOCKET_POS_RIGHT_TOP) -> int:

        socket = JGraphicSocket(
            self._parentNode, self._socketCount, GRSOCKET_TYPE_OUTPUT
        )

        socket.setPos(self.CalcSocketPos(len(self._outSocketsList), position))

        self._outSocketsList.append(socket)
        self._socketCount += 1
        return self._socketCount - 1

    def CalcSocketPos(self, index: int, position: int) -> QPointF:

        # * left posiition
        x = 0

        # * right posiition
        if position in [GRSOCKET_POS_RIGHT_BOTTOM, GRSOCKET_POS_RIGHT_TOP]:
            x = self._parentNode.nodeWidth

        # * top position
        vertPadding = (
            self._parentNode._titleHeight
            + self._parentNode._titlePadding
            + self._parentNode._edgeSize
        )
        y = vertPadding + index * self._socketSpacing

        # * bottom position
        if position in [GRSOCKET_POS_LEFT_BOTTOM, GRSOCKET_POS_RIGHT_BOTTOM]:
            y = self._parentNode.nodeHeight - vertPadding - index * self._socketSpacing

        return QPointF(x, y)
