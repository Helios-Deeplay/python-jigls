from jeditor.core.graphicedgepath import (
    JGraphicEdgeBezier,
    JGraphicEdgeDirect,
    JGraphicEdgeSquare,
)
from jeditor.core.graphicsocket import JGraphicSocket
from jeditor.core.constants import (
    GREDGE_COLOR_DEFAULT,
    GREDGE_COLOR_SELECTED,
    GREDGE_PATH_BEZIER,
    GREDGE_PATH_DIRECT,
    GREDGE_PATH_SQUARE,
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


class JGraphicEdge(QGraphicsPathItem):
    def __init__(
        self,
        startSocket: Optional[JGraphicSocket],
        destinationSocket: Optional[JGraphicSocket],
        parent: Optional[QGraphicsPathItem] = None,
        edgePathType: int = GREDGE_PATH_DIRECT,
        tempDragPos: QtCore.QPointF = QtCore.QPointF(),
    ) -> None:
        super().__init__(parent=parent)

        self._startSocket: Optional[JGraphicSocket] = startSocket
        self._destinationSocket: Optional[JGraphicSocket] = destinationSocket
        self._edgePathType: int = edgePathType
        self._tempDragPos: QtCore.QPointF = tempDragPos

        self._InitVariables()
        self.initUI()

    @property
    def destinationSocket(self):
        return self._destinationSocket

    @destinationSocket.setter
    def destinationSocket(self, value: Optional[JGraphicSocket]) -> None:
        self._destinationSocket = value
        self._destinationSocket.edgeList = self

    @property
    def tempDragPos(self) -> QtCore.QPointF:
        return QtCore.QPointF()

    @tempDragPos.setter
    def tempDragPos(self, value: QtCore.QPointF):
        self._tempDragPos = value

    @property
    def sourcePos(self):
        return self._startSocket.scenePos()

    @property
    def destinationPos(self):
        if self._destinationSocket is not None:
            return self._destinationSocket.scenePos()
        return self._tempDragPos

    @property
    def edgePathType(self):
        return self._edgePathType

    @edgePathType.setter
    def edgePathType(self, value: int) -> None:
        self._edgePathType = value

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

        self._startSocket.edgeList = self
        if self._destinationSocket is not None:
            self._destinationSocket.edgeList = self

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
            self._startSocket.RemoveEdge(self)
        if self._destinationSocket is not None:
            self._destinationSocket.RemoveEdge(self)
        self._startSocket = None
        self._destinationSocket = None

    def UpdatePath(self, *args, **kwargs):
        if self.edgePathType == GREDGE_PATH_DIRECT:
            self.setPath(
                JGraphicEdgeDirect.GetPath(self.sourcePos, self.destinationPos)
            )
        elif self.edgePathType == GREDGE_PATH_BEZIER:
            self.setPath(
                JGraphicEdgeBezier.GetPath(self.sourcePos, self.destinationPos)
            )
        else:
            self.setPath(
                JGraphicEdgeSquare.GetPath(self.sourcePos, self.destinationPos)
            )

    def __del__(self):
        self.RemoveFromSockets()
