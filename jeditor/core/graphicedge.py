from jeditor.core.graphicsocket import JGraphicSocket
from jeditor.core.constants import (
    GREDGE_COLOR_DEFAULT,
    GREDGE_COLOR_SELECTED,
    GREDGE_WIDTH,
)
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QStyleOptionGraphicsItem,
    QWidget,
)


class JGraphicEdgeBase(QGraphicsPathItem):
    def __init__(
        self,
        startSocket: JGraphicSocket,
        endSocket: JGraphicSocket,
        parent: Optional[QGraphicsPathItem] = None,
    ) -> None:
        super().__init__(parent=parent)

        self._startSocket: Optional[JGraphicSocket] = startSocket
        self._endSocket: Optional[JGraphicSocket] = endSocket

        self._InitVariables()
        self.initUI()

    @property
    def sourcePos(self):
        return self._startSocket.scenePos()

    @property
    def destinationPos(self):
        return self._endSocket.scenePos()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(-1.0)

    def _InitVariables(self):
        self._edgeColor = QtGui.QColor(GREDGE_COLOR_DEFAULT)
        self._edgeColorSelected = QtGui.QColor(GREDGE_COLOR_SELECTED)
        self._edgePen = QtGui.QPen(self._edgeColor)
        self._edgePenSelected = QtGui.QPen(self._edgeColorSelected)
        self._edgePen.setWidthF(GREDGE_WIDTH)
        self._edgePenSelected.setWidthF(GREDGE_WIDTH)
        self._startSocket.edge = self
        if self._endSocket is not None:
            self._endSocket.edge = self

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        self.UpdatePath()
        painter.setPen(self._edgePenSelected if self.isSelected() else self._edgePen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

    def RemoveFromSockets(self):
        if self._startSocket is not None:
            self._startSocket.edge = None
        if self._endSocket is not None:
            self._endSocket.edge = None
        self._startSocket = None
        self._endSocket = None

    def UpdatePath(self, *args, **kwargs):
        raise NotImplementedError
