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
        source: QtCore.QPointF,
        destination: QtCore.QPointF,
        parent: Optional[QGraphicsPathItem] = None,
    ) -> None:
        super().__init__(parent=parent)

        self.posSource = source
        self.posDest = destination

        self._InitVariables()
        self.initUI()

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

    def UpdatePath(self, *args, **kwargs):
        raise NotImplementedError
