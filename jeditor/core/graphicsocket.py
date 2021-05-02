from typing import Optional

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

from .constants import (
    GRSOCKET_COLOR_BACKGROUND,
    GRSOCKET_COLOR_OUTLINE,
    GRSOCKET_RADIUS,
    GRSOCKET_WIDTH_OUTLINE,
)

try:
    from .graphicedge import JGraphicEdgeBase
except Exception as e:
    pass


class JGraphicSocket(QGraphicsItem):
    def __init__(
        self,
        parent: QGraphicsItem,
        index: int,
        type: int,
        edge=None,
    ) -> None:
        super().__init__(parent=parent)

        self.node = parent
        self.index = index
        self.socketType = type
        self._edge: Optional[JGraphicEdgeBase] = edge

        self._InitVariables()
        self.initUI()

    def _InitVariables(self):
        self._radius = GRSOCKET_RADIUS
        self._colorOutline = QtGui.QColor(GRSOCKET_COLOR_OUTLINE)
        self._colorBackground = QtGui.QColor(GRSOCKET_COLOR_BACKGROUND)
        self._penSocket = QtGui.QPen(self._colorOutline)
        self._brushSocket = QtGui.QBrush(self._colorBackground)
        self._penSocket.setWidthF(GRSOCKET_WIDTH_OUTLINE)
        self._penSelected: QtGui.QPen = QtGui.QPen(QtGui.QColor(QtCore.Qt.red))

    def initUI(self):
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        painter.setPen(self._penSocket if not self.isSelected() else self._penSelected)
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
    def edge(self):
        return self._edge

    @edge.setter
    def edge(self, value) -> None:
        self._edge = value

    def HasEdge(self):
        return True if self._edge is not None else False
