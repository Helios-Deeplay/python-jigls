from typing import List
from .constants import (
    GRSCENE_BACKGROUND_COLOR,
    GRSCENE_GRID_SIZE,
    GRSCENE_LINE_SPACING,
    GRSCENE_MAJOR_LINE_COLOR,
    GRSCENE_MAJOR_LINE_PEN_WIDTH,
    GRSCENE_MINOR_LINE_COLOR,
    GRSCENE_MINOR_LINE_PEN_WIDTH,
    GRSCENE_WIDTH,
)
from PyQt5 import QtGui, QtWidgets, QtCore
import math


class JiglsGraphicScene(QtWidgets.QGraphicsScene):
    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._InitVariables()

        self._penMajorLine.setWidth(self._widhtMajorLine)
        self._penMinorLine.setWidth(self._widhtMinorLine)

        self.setBackgroundBrush(self._colorBackground)

    def SetGrSceneWH(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def _InitVariables(self):

        # * colors
        self._colorBackground = QtGui.QColor(GRSCENE_BACKGROUND_COLOR)
        self._colorMajorLine = QtGui.QColor(GRSCENE_MAJOR_LINE_COLOR)
        self._colorMinorLine = QtGui.QColor(GRSCENE_MINOR_LINE_COLOR)

        # * pen
        self._widhtMajorLine: int = GRSCENE_MAJOR_LINE_PEN_WIDTH
        self._widhtMinorLine: int = GRSCENE_MINOR_LINE_PEN_WIDTH
        self._penMajorLine = QtGui.QPen(self._colorMajorLine)
        self._penMinorLine = QtGui.QPen(self._colorMinorLine)

        # * line grid and spacing
        self._gridSize: int = GRSCENE_GRID_SIZE
        self._lineSpacing: int = GRSCENE_LINE_SPACING

    def drawBackground(
        self, painter: QtGui.QPainter, rect: QtCore.QRectF
    ) -> None:
        super().drawBackground(painter, rect)

        # * grid bounds
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        fLeft = left - (left % self._gridSize)
        fTop = top - (top % self._gridSize)

        # * compute lines
        majorLine = [
            QtCore.QLine(x, top, x, bottom)
            for x in range(
                fLeft, right, self._gridSize * self._lineSpacing
            )
        ]

        for y in range(fTop, bottom, self._gridSize * self._lineSpacing):
            majorLine.append(QtCore.QLine(left, y, right, y))

        minorLines = [
            QtCore.QLine(x, top, x, bottom)
            for x in range(fLeft, right, self._gridSize)
        ]

        for y in range(fTop, bottom, self._gridSize):
            minorLines.append(QtCore.QLine(left, y, right, y))

        # * draw lines
        painter.setPen(self._penMajorLine)
        for line in majorLine:
            painter.drawLine(line)

        painter.setPen(self._penMinorLine)
        for line in minorLines:
            painter.drawLine(line)
