from typing import List, Optional, Set

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from .constants import (
    GRSOCKET_COLOR_BACKGROUND,
    GRSOCKET_COLOR_HOVER,
    GRSOCKET_COLOR_OUTLINE,
    GRSOCKET_MULTI_CONNECTION,
    GRSOCKET_RADIUS,
    GRSOCKET_WIDTH_OUTLINE,
)

try:
    from .graphicedge import JGraphicEdge
except Exception as e:
    pass


class JGraphicSocket(QGraphicsItem):
    def __init__(
        self,
        parent: QGraphicsItem,
        index: int,
        socketType: int,
        multiConnectionType: bool = GRSOCKET_MULTI_CONNECTION,
    ) -> None:
        super().__init__(parent=parent)

        self.node: QGraphicsItem = parent
        self.index: int = index
        self.socketType: int = socketType
        self._edgeList: Set[Optional[JGraphicEdge]] = set()
        self._multiConnectionType: bool = multiConnectionType

        self._InitVariables()
        self.initUI()

    def _InitVariables(self):
        self._radius = GRSOCKET_RADIUS
        self._colorOutline = QtGui.QColor(GRSOCKET_COLOR_OUTLINE)
        self._colorBackground = QtGui.QColor(GRSOCKET_COLOR_BACKGROUND)
        self._penOutline = QtGui.QPen(self._colorOutline)
        self._brushSocket = QtGui.QBrush(self._colorBackground)
        self._penOutline.setWidthF(GRSOCKET_WIDTH_OUTLINE)
        self._colorHover = QtGui.QColor(GRSOCKET_COLOR_HOVER)

    def initUI(self):
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        painter.setPen(
            self._penOutline
        )  # if not self.isSelected() else self._penSelected)
        painter.setBrush(self._brushSocket)
        painter.drawEllipse(
            int(-self._radius),
            int(-self._radius),
            int(2 * self._radius),
            int(2 * self._radius),
        )

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            int(-self._radius),
            int(-self._radius),
            int(2 * self._radius),
            int(2 * self._radius),
        )

    @property
    def multiConnectionType(self):
        return self._multiConnectionType

    @property
    def edgeList(self):
        return self._edgeList

    @edgeList.setter
    def edgeList(self, value) -> None:
        assert value is not None
        self._edgeList.add(value)

    def RemoveEdge(self, edge):
        # assert isinstance(edge, JGraphicEdge)
        self._edgeList.discard(edge)

    def HasEdge(self, edge) -> bool:
        # assert isinstance(edge, JGraphicEdge)
        return True if edge in self._edgeList else False

    def CanAddEdge(self) -> bool:
        if self._multiConnectionType:
            return True
        elif not self._multiConnectionType and len(self._edgeList) == 0:
            return True
        else:
            return False

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self._penOutline.setColor(self._colorHover)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._penOutline.setColor(self._colorOutline)
        super().hoverLeaveEvent(event)
