import logging
from typing import List, Optional, Set, TYPE_CHECKING

from jeditor.logger import logger
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
    GRSOCKET_RADIUS,
    GRSOCKET_WIDTH_OUTLINE,
)
from .graphicedge import JGraphicEdge

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from .graphicnode import JGraphicNode


class JGraphicSocket(QGraphicsItem):
    def __init__(
        self,
        parent: "JGraphicNode",
        index: int,
        socketType: int,
        multiConnection: bool = True,
    ) -> None:
        super().__init__(parent=parent)

        self.parentNodeID: str = parent.nodeIdentifier
        self.index: int = index
        self.socketType: int = socketType
        self._multiConnection: bool = multiConnection

        self.initUI()

    def initUI(self):
        self._radius = GRSOCKET_RADIUS
        self._colorOutline = QtGui.QColor(GRSOCKET_COLOR_OUTLINE)
        self._colorBackground = QtGui.QColor(GRSOCKET_COLOR_BACKGROUND)
        self._penOutline = QtGui.QPen(self._colorOutline)
        self._brushSocket = QtGui.QBrush(self._colorBackground)
        self._penOutline.setWidthF(GRSOCKET_WIDTH_OUTLINE)
        self._colorHover = QtGui.QColor(GRSOCKET_COLOR_HOVER)
        self._edgeList: Set[Optional[JGraphicEdge]] = set()
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
        if self._multiConnection:
            painter.drawRect(
                int(-self._radius),
                int(-self._radius),
                int(2 * self._radius),
                int(2 * self._radius),
            )
        else:
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
    def multiConnection(self):
        return self._multiConnection

    @property
    def edgeList(self) -> List[Optional[JGraphicEdge]]:
        return list(self._edgeList)

    def AddEdge(self, edge: JGraphicEdge) -> None:
        assert edge is not None
        assert not self.AtMaxEdgeLimit(), logger.warning("max edge limit reached")
        self._edgeList.add(edge)

    def RemoveEdge(self, edge: JGraphicEdge):
        self._edgeList.discard(edge)

    def EdgeCount(self) -> int:
        return len(self._edgeList)

    def HasEdge(self, edge: JGraphicEdge) -> bool:
        assert edge is not None
        return True if edge in self._edgeList else False

    def AtMaxEdgeLimit(self) -> bool:
        if self._multiConnection:
            return False
        # * can add one edge to single connection type
        elif not self._multiConnection and len(self._edgeList) == 0:
            return False
        else:
            return True

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self._penOutline.setColor(self._colorHover)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._penOutline.setColor(self._colorOutline)
        super().hoverLeaveEvent(event)
