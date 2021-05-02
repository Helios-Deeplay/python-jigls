import typing
from .socketmanager import JNodeSocketManager
from .contentwidget import JNodeContent
from .constants import (
    GRNODE_COLOR_BACKGROUND,
    GRNODE_COLOR_DEFAULT,
    GRNODE_COLOR_SELECTED,
    GRNODE_COLOR_TITLE,
    GRNODE_EDGE_SIZE,
    GRNODE_NODE_HEIGHT,
    GRNODE_NODE_WIDHT,
    GRNODE_TITLE_COLOR,
    GRNODE_TITLE_FONT,
    GRNODE_TITLE_FONT_SIZE,
    GRNODE_TITLE_HEIGHT,
    GRNODE_TITLE_PADDING,
)
from .graphicscene import JiglsGraphicScene
from typing import List, Optional, Tuple
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsSceneMouseEvent,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget,
)


class JGraphicNode(QGraphicsItem):
    def __init__(
        self,
        parent: Optional[QGraphicsItem] = None,
        nodeContent: Optional[JNodeContent] = None,
        title: str = "Base Node",
        inSockets=1,
        outSockets=1,
    ) -> None:
        super().__init__(parent=parent)

        self._InitVariables()
        self.initUI()

        self.InitTitle(title)
        self._InitContent(nodeContent)

        self.socketManager = JNodeSocketManager(self, inSockets, outSockets)

    def initUI(self):
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        # self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        return super().itemChange(change, value)

    def _InitVariables(self):
        self._titleColor = QtCore.Qt.white
        self._titleFont: QtGui.QFont = QtGui.QFont(
            GRNODE_TITLE_FONT, GRNODE_TITLE_FONT_SIZE
        )
        self._nodeWidth: int = GRNODE_NODE_WIDHT
        self._nodeHeight: int = GRNODE_NODE_HEIGHT
        self._titleHeight: float = GRNODE_TITLE_HEIGHT
        self._titleBrush: QtGui.QBrush = QtGui.QBrush(QtGui.QColor(GRNODE_COLOR_TITLE))
        self._titlePadding: int = GRNODE_TITLE_PADDING
        self._edgeSize: float = GRNODE_EDGE_SIZE
        self._penDefault: QtGui.QPen = QtGui.QPen(QtGui.QColor(GRNODE_COLOR_DEFAULT))
        self._penSelected: QtGui.QPen = QtGui.QPen(QtGui.QColor(GRNODE_COLOR_SELECTED))
        self._brushBackground: QtGui.QBrush = QtGui.QBrush(
            QtGui.QColor(GRNODE_COLOR_BACKGROUND)
        )
        self._graphicsContent: QGraphicsProxyWidget = QGraphicsProxyWidget(self)

        self._titleItem: QGraphicsTextItem = QGraphicsTextItem(self)

    def InitTitle(self, title: str):
        self._titleItem.setDefaultTextColor(self._titleColor)
        self._titleItem.setFont(self._titleFont)
        self._titleItem.setPos(self._titlePadding, 0)
        self._titleItem.setTextWidth(self._nodeWidth - 2 * self._titlePadding)
        self._titleItem.setPlainText(title)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        self._titleItem.setPlainText(value)

    @property
    def nodeWidth(self):
        return self._nodeWidth

    @property
    def nodeHeight(self):
        return self._nodeHeight

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            0,
            0,
            self._nodeWidth,
            self._nodeHeight,
        )

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionGraphicsItem,
        widget: Optional[QWidget],
    ) -> None:

        # ? title
        titlePath = QtGui.QPainterPath()
        titlePath.setFillRule(QtCore.Qt.WindingFill)

        titlePath.addRoundedRect(
            0,
            0,
            self._nodeWidth,
            self._titleHeight,
            self._edgeSize,
            self._edgeSize,
        )

        titlePath.addRect(
            0,
            self._titleHeight - self._edgeSize,
            self._edgeSize,
            self._edgeSize,
        )

        titlePath.addRect(
            self._nodeWidth - self._edgeSize,
            self._titleHeight - self._edgeSize,
            self._edgeSize,
            self._edgeSize,
        )

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._titleBrush)
        painter.drawPath(titlePath.simplified())

        # ? content
        ContentPath = QtGui.QPainterPath()
        ContentPath.setFillRule(QtCore.Qt.WindingFill)
        ContentPath.addRoundedRect(
            0,
            self._titleHeight,
            self._nodeWidth,
            self._nodeHeight - self._titleHeight,
            self._edgeSize,
            self._edgeSize,
        )
        ContentPath.addRect(0, self._titleHeight, self._edgeSize, self._edgeSize)
        ContentPath.addRect(
            self._nodeWidth - self._edgeSize,
            self._titleHeight,
            self._edgeSize,
            self._edgeSize,
        )
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._brushBackground)
        painter.drawPath(ContentPath.simplified())

        # ? outline
        outline = QtGui.QPainterPath()
        outline.addRoundedRect(
            0,
            0,
            self._nodeWidth,
            self._nodeHeight,
            self._edgeSize,
            self._edgeSize,
        )

        painter.setPen(self._penDefault if not self.isSelected() else self._penSelected)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(outline.simplified())

    def _InitContent(self, nodeContent: Optional[JNodeContent]):
        self.nodeContent = nodeContent

        if self.nodeContent is not None:
            self.nodeContent.setGeometry(
                int(self._edgeSize),
                int(self._titleHeight + self._edgeSize),
                int(self._nodeWidth - 2 * self._edgeSize),
                int(self._nodeHeight - 2 * self._edgeSize - self._titleHeight),
            )
            self._graphicsContent.setWidget(self.nodeContent)
