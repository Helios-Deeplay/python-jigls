from .graphicedge import JGraphicEdgeBase

from PyQt5 import QtCore, QtGui


class JGraphicEdgeDirect(JGraphicEdgeBase):
    def UpdatePath(self):
        s = self.sourcePos
        d = self.destinationPos

        path = QtGui.QPainterPath(s)
        path.lineTo(d)
        self.setPath(path)


class JGraphicEdgeSquare(JGraphicEdgeBase):
    def UpdatePath(self, *args, hndWeight=0.5, **kwargs):
        s = self.sourcePos
        d = self.destinationPos

        mid_x = s.x() + ((d.x() - s.x()) * hndWeight)

        path = QtGui.QPainterPath(QtCore.QPointF(s.x(), s.y()))
        path.lineTo(mid_x, s.y())
        path.lineTo(mid_x, d.y())
        path.lineTo(d.x(), d.y())
        self.setPath(path)


class JGraphicEdgeBezier(JGraphicEdgeBase):
    def UpdatePath(self):
        s = self.sourcePos
        d = self.destinationPos

        dist = abs(s.x() - d.x()) // 2

        path = QtGui.QPainterPath(QtCore.QPointF(s.x(), s.y()))
        path.cubicTo(s.x() + dist, s.y(), d.x() - dist, d.y(), d.x(), d.y())
        self.setPath(path)