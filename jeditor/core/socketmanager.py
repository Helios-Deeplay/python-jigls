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


class JNodeSocketManager:
    def __init__(self, parent) -> None:

        self._parentNode: JGraphicNode = parent

        self._inSocketsList: List[JGraphicSocket] = []
        self._outSocketsList: List[JGraphicSocket] = []

        self._InitVariables()

    def _InitVariables(self):
        self._socketSpacing = GRSOCKET_SPACING
        self._socketCount: int = 0

    @property
    def inSocketCount(self) -> int:
        return len(self._inSocketsList)

    @property
    def outSocketCount(self) -> int:
        return len(self._outSocketsList)

    @property
    def socketCount(self) -> int:
        return self._socketCount

    def GetInputSocketByIndex(self, index: int) -> JGraphicSocket:
        assert index <= len(self._inSocketsList)
        return self._inSocketsList[index]

    def GetOutputSocketByIndex(self, index: int) -> JGraphicSocket:
        assert index <= len(self._outSocketsList)
        return self._outSocketsList[index]

    def GetInputSocketPosByIndex(self, index: int) -> QPointF:
        assert index <= len(self._inSocketsList)
        return self.GetInputSocketByIndex(index).pos()

    def GetOutputSocketPosByIndex(self, index: int) -> QPointF:
        assert index <= len(self._outSocketsList)
        return self.GetOutputSocketByIndex(index).pos()

    def AddSocket(self, type, multiConnection: bool = True) -> int:
        if type == GRSOCKET_TYPE_INPUT:
            return self.AddInputSocket(multiConnection=multiConnection)
        elif type == GRSOCKET_TYPE_OUTPUT:
            return self.AddOutputSocket(multiConnection=multiConnection)
        else:
            return -1

    def AddInputSocket(
        self, multiConnection: bool = True, position=GRSOCKET_POS_LEFT_BOTTOM
    ) -> int:

        socket = JGraphicSocket(
            parent=self._parentNode,
            index=self._socketCount,
            socketType=GRSOCKET_TYPE_INPUT,
            multiConnection=multiConnection,
        )

        socket.setPos(self._CalculateSocketPos(len(self._inSocketsList), position))

        self._inSocketsList.append(socket)
        self._socketCount += 1
        return self._socketCount - 1

    def AddOutputSocket(
        self, multiConnection: bool = True, position=GRSOCKET_POS_RIGHT_TOP
    ) -> int:

        socket = JGraphicSocket(
            parent=self._parentNode,
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
