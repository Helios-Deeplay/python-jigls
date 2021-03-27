from typing import Optional
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QWidget,
)


class JigleGraphicSocket(QGraphicsItem):

    _Radius_ = 9.0
    _OutlineWidth_ = 3.0
    _ColorOutline_ = QtGui.QColor("#FF000000")
    _ColorBakcground_ = QtGui.QColor("#FFFF7700")
    _SocketPen_ = QtGui.QPen(_ColorOutline_)
    _SocketBrush_ = QtGui.QBrush(_ColorBakcground_)

    def __init__(self, parent: QGraphicsItem, index: int) -> None:
        super().__init__(parent=parent)

        self.node = parent
        self.index = index
        self._SocketPen_.setWidthF(self._OutlineWidth_)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        painter.setPen(self._SocketPen_)
        painter.setBrush(self._SocketBrush_)
        painter.drawEllipse(
            int(-self._Radius_),
            int(-self._Radius_),
            int(2 * self._Radius_),
            int(2 * self._Radius_),
        )

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            int(-self._Radius_),
            int(-self._Radius_),
            int(2 * self._Radius_),
            int(2 * self._Radius_),
        )
