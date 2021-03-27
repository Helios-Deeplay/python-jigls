from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

from jiglsgui.graphicsocket import JigleGraphicSocket
from jiglsgui.scene import JigleScene
from jiglsgui.webelementcontent import JigleWebElementContent


class JigleGraphicEdge(QGraphicsPathItem):

    _EdgeColor_ = QtGui.QColor("#001000")
    _EdgeColorSelected_ = QtGui.QColor("#00FF00")
    _EdgePen_ = QtGui.QPen(_EdgeColor_)
    _EdgePenSelected_ = QtGui.QPen(_EdgeColorSelected_)

    def __init__(
        self,
        edge,
        parent: Optional[QGraphicsPathItem] = None,
    ) -> None:
        super().__init__(parent=parent)

        self.edge = edge
        self.posSource = (0, 0)
        self.posDest = (200, 100)

        self.initUI()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        self.UpdatePath()
        painter.setPen(
            self._EdgePenSelected_ if self.isSelected() else self._EdgePen_
        )
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

    def UpdatePath(self):
        raise NotImplementedError("must be overwritten")


class JigleGraphicEdgeBezier(JigleGraphicEdge):
    def UpdatePath(self):
        s = self.posSource
        d = self.posDest

        dist = abs(s[0] - d[0]) // 2
        path = QtGui.QPainterPath(QtCore.QPointF(s[0], s[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1], d[0], d[1])
        self.setPath(path)
