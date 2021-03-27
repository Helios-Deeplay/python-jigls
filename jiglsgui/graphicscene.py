import typing
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QPen
import math


class JiglsGraphicScene(QtWidgets.QGraphicsScene):

    _BackgroudColor_ = QColor("#393939")
    _MajorLineColor_ = QColor("292929")
    _MinorLineColor_ = QColor("2f2f2f")

    def __init__(
        self,
        scene,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.scene = scene

        self.gridSize = 20
        self.lineSpacing = 5

        self.MajorLinePen = QPen(self._MajorLineColor_)
        self.MajorLinePen.setWidth(2)

        self.MinorLinePen = QPen(self._MinorLineColor_)
        self.MinorLinePen.setWidth(1)

        self.setBackgroundBrush(self._BackgroudColor_)

    def SetGrScene(self, width, height):
        self.setSceneRect(
            -width // 2,
            -height // 2,
            width,
            height,
        )

    def drawBackground(
        self, painter: QtGui.QPainter, rect: QtCore.QRectF
    ) -> None:
        super().drawBackground(painter, rect)

        # * grid bounds

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        fLeft = left - (left % self.gridSize)
        fTop = top - (top % self.gridSize)

        # * compute lines

        majorLine = [
            QtCore.QLine(x, top, x, bottom)
            for x in range(fLeft, right, self.gridSize * self.lineSpacing)
        ]

        for y in range(fTop, bottom, self.gridSize * self.lineSpacing):
            majorLine.append(QtCore.QLine(left, y, right, y))

        minorLines = [
            QtCore.QLine(x, top, x, bottom)
            for x in range(fLeft, right, self.gridSize)
        ]

        for y in range(fTop, bottom, self.gridSize):
            minorLines.append(QtCore.QLine(left, y, right, y))

        # * draw lines

        painter.setPen(self.MajorLinePen)
        for line in majorLine:
            painter.drawLine(line)

        painter.setPen(self.MinorLinePen)
        for line in minorLines:
            painter.drawLine(line)
