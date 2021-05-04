import logging
from typing import Optional

from jeditor.core.constants import (
    GREDGE_COLOR_DEFAULT,
    GREDGE_COLOR_DRAG,
    GREDGE_COLOR_SELECTED,
    GREDGE_PATH_BEZIER,
    GREDGE_PATH_DIRECT,
    GREDGE_PATH_SQUARE,
    GREDGE_WIDTH,
)
from jeditor.core.graphicedgepath import (
    JGraphicEdgeBezier,
    JGraphicEdgeDirect,
    JGraphicEdgeSquare,
)

try:
    # ? just using for typing. need to resolve circular imports
    from jeditor.core.graphicsocket import JGraphicSocket
except:
    pass
from jeditor.logger import logger
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

logger = logging.getLogger(__name__)


class JGraphicEdge(QGraphicsPathItem):
    def __init__(
        self,
        startSocket,
        destinationSocket,
        parent: Optional[QGraphicsPathItem] = None,
        edgePathType: int = GREDGE_PATH_DIRECT,
    ) -> None:
        super().__init__(parent=parent)

        self._startSocket: JGraphicSocket = startSocket
        self._destinationSocket: Optional[JGraphicSocket] = destinationSocket
        self._edgePathType: int = edgePathType
        self._tempDragPos: QtCore.QPointF = QtCore.QPointF()

        self._InitVariables()
        self.initUI()

    @property
    def startSocket(self):
        return self._startSocket

    @property
    def destinationSocket(self):
        return self._destinationSocket

    @destinationSocket.setter
    def destinationSocket(self, socket) -> None:
        assert not socket.AtMaxEdgeLimit(), logger.warning("max edge limit reached")
        self._destinationSocket = socket
        self._destinationSocket.AddEdge(self)
        self._tempDragPos = QtCore.QPointF()

    @property
    def tempDragPos(self) -> QtCore.QPointF:
        return self._tempDragPos

    @tempDragPos.setter
    def tempDragPos(self, pos: QtCore.QPointF):
        self._tempDragPos = pos
        if self._destinationSocket is not None:
            self._destinationSocket.RemoveEdge(self)
            logger.info("removed edge from destination socket, edge is repositioning")
            self._destinationSocket = None

    @property
    def sourcePos(self):
        return self._startSocket.scenePos()

    @property
    def destinationPos(self) -> QtCore.QPointF:
        if self._destinationSocket is not None:
            return self._destinationSocket.scenePos()
        return self._tempDragPos

    @property
    def endPos(self) -> QtCore.QPointF:
        return self.destinationPos

    @property
    def edgePathType(self) -> int:
        return self._edgePathType

    @edgePathType.setter
    def edgePathType(self, pathType: int) -> None:
        self._edgePathType = pathType

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(-1.0)

    def _InitVariables(self):
        self._edgeColor = QtGui.QColor(GREDGE_COLOR_DEFAULT)
        self._edgeColorSelected = QtGui.QColor(GREDGE_COLOR_SELECTED)
        self._edgeColorDrag = QtGui.QColor(GREDGE_COLOR_DRAG)
        self._edgePen = QtGui.QPen(self._edgeColor)
        self._edgePenSelected = QtGui.QPen(self._edgeColorSelected)
        self._edgePenDrag = QtGui.QPen(self._edgeColorDrag)
        self._edgePen.setWidthF(GREDGE_WIDTH)
        self._edgePenSelected.setWidthF(GREDGE_WIDTH)
        self._edgePenDrag.setWidthF(GREDGE_WIDTH)
        self._edgePenDrag.setStyle(QtCore.Qt.DashLine)

        self._startSocket.AddEdge(self)
        if self._destinationSocket is not None:
            self._destinationSocket.AddEdge(self)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        painter.setPen(self._edgePenSelected if self.isSelected() else self._edgePen)
        if self.destinationSocket is None:
            painter.setPen(self._edgePenDrag)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

        self.UpdatePath()

    def RemoveFromSockets(self):
        if self._startSocket is not None:
            self._startSocket.RemoveEdge(self)
        if self._destinationSocket is not None:
            self._destinationSocket.RemoveEdge(self)

    def UpdatePath(self, *args, **kwargs):
        if self.edgePathType == GREDGE_PATH_DIRECT:
            self.setPath(
                JGraphicEdgeDirect.GetPath(self.sourcePos, self.destinationPos)
            )
        elif self.edgePathType == GREDGE_PATH_BEZIER:
            self.setPath(
                JGraphicEdgeBezier.GetPath(self.sourcePos, self.destinationPos)
            )
        elif self.edgePathType == GREDGE_PATH_SQUARE:
            self.setPath(
                JGraphicEdgeSquare.GetPath(self.sourcePos, self.destinationPos)
            )
        else:
            logger.error("unknown edge path type, defaulting direct")
            self.setPath(
                JGraphicEdgeDirect.GetPath(self.sourcePos, self.destinationPos)
            )
