from jiglsgui.graphicscene import JiglsGraphicScene
from jiglsgui.graphicsocket import JigleGraphicSocket
from jiglsgui.webelementcontent import JigleWebElementContent
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


class JigleGraphicNode(QGraphicsItem):

    _TitleColor_ = QtCore.Qt.white
    _TitleFont_ = QtGui.QFont("Ubuntu", 10)
    _Width_ = 180
    _Height_ = 240
    _TitleHeight_ = 24.0
    _EdgeSize_ = 10.0
    _PenDefault_ = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
    _PenSelected_ = QtGui.QPen(QtGui.QColor(QtCore.Qt.green))
    _BrushTitle_ = QtGui.QBrush(QtGui.QColor("#FF313131"))
    _BrushBackground_ = QtGui.QBrush(QtGui.QColor("#E3232323"))
    _TitlePadding_ = 20

    _InputSocket_ = 1
    _OutputSocket_ = 2

    def __init__(
        self,
        scene: Optional[JiglsGraphicScene] = None,
        parent: Optional[QGraphicsItem] = None,
        title: str = "Web Element",
    ) -> None:
        super().__init__(parent=parent)

        # self.grScene = scene.grScene
        self.content = JigleWebElementContent()

        self.initTitle()
        self.title = title

        self.initContent()
        self.initSocket()

        self.initUI()

    def initUI(self):
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def initTitle(self):
        self.titleItem = QGraphicsTextItem(self)
        self.titleItem.setDefaultTextColor(self._TitleColor_)
        self.titleItem.setFont(self._TitleFont_)
        self.titleItem.setPos(self._TitlePadding_, 0)
        self.titleItem.setTextWidth(self._Width_ - 2 * self._TitlePadding_)

    def initContent(self):
        if self.content is not None:
            self.content.setGeometry(
                int(self._EdgeSize_),
                int(self._TitleHeight_ + self._EdgeSize_),
                int(self._Width_ - 2 * self._EdgeSize_),
                int(
                    self._Height_
                    - 2 * self._EdgeSize_
                    - self._TitleHeight_
                ),
            )

        self.grContent = QGraphicsProxyWidget(self)
        self.grContent.setWidget(self.content)

    def initSocket(self):
        self.InputSocket = JigleGraphicSocket(self, self._InputSocket_)
        self.OutputSocket = JigleGraphicSocket(self, self._OutputSocket_)

        self.InputSocket.setPos(*self.GrSocketPosition(self._InputSocket_))
        self.OutputSocket.setPos(
            *self.GrSocketPosition(self._OutputSocket_)
        )

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        self.titleItem.setPlainText(self._title)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            0 + 0.5,
            0 + 0.5,
            self._Width_ - 0.5,
            self._Height_ - 0.5,
        )

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        self.setPos(event.scenePos())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

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
            self._Width_,
            self._TitleHeight_,
            self._EdgeSize_,
            self._EdgeSize_,
        )

        titlePath.addRect(
            0,
            self._TitleHeight_ - self._EdgeSize_,
            self._EdgeSize_,
            self._EdgeSize_,
        )

        titlePath.addRect(
            self._Width_ - self._EdgeSize_,
            self._TitleHeight_ - self._EdgeSize_,
            self._EdgeSize_,
            self._EdgeSize_,
        )

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._BrushTitle_)
        painter.drawPath(titlePath.simplified())

        # ? content
        ContentPath = QtGui.QPainterPath()
        ContentPath.setFillRule(QtCore.Qt.WindingFill)
        ContentPath.addRoundedRect(
            0,
            self._TitleHeight_,
            self._Width_,
            self._Height_ - self._TitleHeight_,
            self._EdgeSize_,
            self._EdgeSize_,
        )
        ContentPath.addRect(
            0, self._TitleHeight_, self._EdgeSize_, self._EdgeSize_
        )
        ContentPath.addRect(
            self._Width_ - self._EdgeSize_,
            self._TitleHeight_,
            self._EdgeSize_,
            self._EdgeSize_,
        )
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._BrushBackground_)
        painter.drawPath(ContentPath.simplified())

        # ? outline
        outline = QtGui.QPainterPath()
        outline.addRoundedRect(
            0,
            0,
            self._Width_,
            self._Height_,
            self._EdgeSize_,
            self._EdgeSize_,
        )

        painter.setPen(
            self._PenDefault_
            if not self.isSelected()
            else self._PenSelected_
        )
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(outline.simplified())

    def GrSocketPosition(self, type):
        x = 0 if type == self._InputSocket_ else self._Width_
        y = self._Height_ / 2
        return float(x), float(y)
