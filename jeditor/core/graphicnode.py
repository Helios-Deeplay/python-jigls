from jeditor.core.graphicsocket import JGraphicSocket
from .contentwidget import JNodeContent
from .constants import (
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
from typing import Optional
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
    ) -> None:
        super().__init__(parent=parent)

        self.initUI()
        self._InitVariables()
        self.InitTitle()
        self._InitContent(nodeContent)
        self.InitSocket()
        self.title = title

    def initUI(self):
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def _InitVariables(self):
        self._titleColor = QtCore.Qt.white
        self._titleFont = QtGui.QFont(
            GRNODE_TITLE_FONT, GRNODE_TITLE_FONT_SIZE
        )
        self._nodeWidth: int = GRNODE_NODE_WIDHT
        self._nodeHeight: int = GRNODE_NODE_HEIGHT
        self._titleHeight: float = GRNODE_TITLE_HEIGHT
        self._titleBrush: QtGui.QBrush = QtGui.QBrush(
            QtGui.QColor("#FF313131")
        )
        self._titlePadding: int = GRNODE_TITLE_PADDING
        self._edgeSize: float = GRNODE_EDGE_SIZE
        self._penDefault: QtGui.QPen = QtGui.QPen(
            QtGui.QColor(QtCore.Qt.black)
        )
        self._penSelected: QtGui.QPen = QtGui.QPen(
            QtGui.QColor(QtCore.Qt.green)
        )
        self._brushBackground: QtGui.QBrush = QtGui.QBrush(
            QtGui.QColor("#E3232323")
        )
        self._graphicsContent: QGraphicsProxyWidget = QGraphicsProxyWidget(
            self
        )

    def InitTitle(self):
        self.titleItem: QGraphicsTextItem = QGraphicsTextItem(self)
        self.titleItem.setDefaultTextColor(self._titleColor)
        self.titleItem.setFont(self._titleFont)
        self.titleItem.setPos(self._titlePadding, 0)
        self.titleItem.setTextWidth(
            self._nodeWidth - 2 * self._titlePadding
        )

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        self.titleItem.setPlainText(value)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            0 + 0.5,
            0 + 0.5,
            self._nodeWidth - 0.5,
            self._nodeHeight - 0.5,
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
        ContentPath.addRect(
            0, self._titleHeight, self._edgeSize, self._edgeSize
        )
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

        painter.setPen(
            self._penDefault
            if not self.isSelected()
            else self._penSelected
        )
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(outline.simplified())

    def _InitContent(self, nodeContent: Optional[JNodeContent]):
        self.nodeContent = nodeContent

        if self.nodeContent is not None:
            self.nodeContent.setGeometry(
                int(self._edgeSize),
                int(self._titleHeight + self._edgeSize),
                int(self._nodeWidth - 2 * self._edgeSize),
                int(
                    self._nodeHeight
                    - 2 * self._edgeSize
                    - self._titleHeight
                ),
            )
            self._graphicsContent.setWidget(self.nodeContent)

    def InitSocket(self):
        self._inputSocket = JGraphicSocket(self, 1)
        # self.OutputSocket = JGraphicSocket(self, self._OutputSocket_)

        # self.InputSocket.setPos(
        #     *self.GraphicNodeSocketPosition(self._InputSocket_)
        # )
        # self.OutputSocket.setPos(
        #     *self.GraphicNodeSocketPosition(self._OutputSocket_)
        # )

    # def GraphicNodeSocketPosition(self, type):
    #     x = 0 if type == self._InputSocket_ else self._nodeWidth
    #     y = self._nodeHeight / 2
    #     return float(x), float(y)
