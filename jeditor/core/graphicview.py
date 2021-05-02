from jeditor.core.graphicedge import JGraphicEdge
from jeditor.core.graphicsocket import JGraphicSocket
import typing
from copy import deepcopy

from .constants import (
    GRSOCKET_MULTI_CONNECTION,
    GRSOCKET_TYPE_INPUT,
    GRSOCKET_TYPE_OUTPUT,
    GRVIEW_HORZ_SCROLLBAR,
    GRVIEW_OP_MODE_DEFAULT,
    GRVIEW_OP_MODE_EDGE_DRAG,
    GRVIEW_OP_MODE_PAN_VIEW,
    GRVIEW_OP_MODE_SELECTION,
    GRVIEW_VERT_SCROLLBAR,
    GRVIEW_ZOOM,
    GRVIEW_ZOOM_CLAMPED,
    GRVIEW_ZOOM_IN_FACTOR,
    GRVIEW_ZOOM_RANGE_MAX,
    GRVIEW_ZOOM_RANGE_MIN,
    GRVIEW_ZOOM_STEP,
)
from PyQt5 import QtCore, QtGui, QtWidgets


class JGraphicView(QtWidgets.QGraphicsView):
    def __init__(
        self,
        scene: QtWidgets.QGraphicsScene,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self.setScene(scene)

        self._InitVariables()

        self.initUI()

    def _InitVariables(self):
        self.scrollbarVert: int = GRVIEW_VERT_SCROLLBAR
        self.scrollbarHorz: int = GRVIEW_HORZ_SCROLLBAR

        self.zoomInFactor: float = GRVIEW_ZOOM_IN_FACTOR
        self.zoomClamped: bool = GRVIEW_ZOOM_CLAMPED
        self.zoom: int = GRVIEW_ZOOM
        self.zoomStep: int = GRVIEW_ZOOM_STEP

        self.zoomRangeMin = GRVIEW_ZOOM_RANGE_MIN
        self.zoomRangeMax = GRVIEW_ZOOM_RANGE_MAX

        self.rubberband: QtWidgets.QRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self.currentState: int = GRVIEW_OP_MODE_DEFAULT

        self.rubberBandStart: QtCore.QPoint = QtCore.QPoint()
        self.origin: QtCore.QPoint = QtCore.QPoint()

        self.__tempSocket: typing.Optional[JGraphicSocket] = None
        self.__tempEdgeDragMode: bool = False
        self.__tempEdgeDragInstance: typing.Optional[JGraphicEdge] = None

    def initUI(self):

        self.setRenderHints(
            QtGui.QPainter.Antialiasing  # type:ignore
            | QtGui.QPainter.HighQualityAntialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
        )

        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        # self.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.MinimalViewportUpdate)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy(self.scrollbarHorz))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy(self.scrollbarVert))
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event: QtGui.QMouseEvent):

        # Drag view
        if event.button() == QtCore.Qt.RightButton:
            self.currentState = GRVIEW_OP_MODE_PAN_VIEW
            self.prevPos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self.setInteractive(False)

        # Rubber band selection
        elif (
            event.button() == QtCore.Qt.LeftButton
            and event.modifiers() == QtCore.Qt.NoModifier
            and self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            is None
        ):
            self.currentState = GRVIEW_OP_MODE_SELECTION
            self._InitRubberband(event.pos())
            self.setInteractive(False)

        # start edge drag
        elif (
            event.button() == QtCore.Qt.LeftButton
            and self.currentState == GRVIEW_OP_MODE_DEFAULT
            and not self.__tempEdgeDragMode
            and isinstance(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()),
                JGraphicSocket,
            )
        ):
            self.currentState = GRVIEW_OP_MODE_EDGE_DRAG
            self.prevPos = event.pos()
            self._StartEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )

        # * end edge drag
        if (
            event.button() == QtCore.Qt.LeftButton
            and self.__tempEdgeDragMode
            and self.currentState != GRVIEW_OP_MODE_EDGE_DRAG
        ):
            self._EndEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )

        # * debug
        if event.button() == QtCore.Qt.MidButton:
            for item in self.scene().items():
                if isinstance(item, JGraphicEdge):
                    print(type(item))
            print("-" * 10)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):

        # Drag canvas.
        if self.currentState == GRVIEW_OP_MODE_EDGE_DRAG:
            offset = self.prevPos - event.pos()  # type:ignore
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + offset.y()
            )
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + offset.x()
            )

        # RuberBand selection.
        elif self.currentState == GRVIEW_OP_MODE_SELECTION:
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized()
            )

        # Edge drag
        elif self.__tempEdgeDragMode:
            self.__tempEdgeDragInstance.tempDragPos = self.mapToScene(event.pos())
            self.__tempEdgeDragInstance.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):

        # Drag
        if self.currentState == GRVIEW_OP_MODE_PAN_VIEW:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)

        # Selection.
        elif self.currentState == GRVIEW_OP_MODE_SELECTION:
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized()
            )
            painterPath = self._ReleaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)

        self.currentState = GRVIEW_OP_MODE_DEFAULT

        # # * debug
        # if event.button() == QtCore.Qt.LeftButton:
        #     for item in self.scene().items():
        #         print(type(item))
        #     print("-" * 10)

        super().mouseReleaseEvent(event)

    def _InitRubberband(self, position: QtCore.QPoint):
        self.rubberBandStart = position
        self.origin = position
        self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()

    def _ReleaseRubberband(self):
        painterPath = QtGui.QPainterPath()
        rect = self.mapToScene(self.rubberband.geometry())
        painterPath.addPolygon(rect)
        self.rubberband.hide()
        return painterPath

    def wheelEvent(self, event: QtGui.QWheelEvent):
        zoomOutFactor = 1 / self.zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRangeMin:
            self.zoom, clamped = self.zoomRangeMin, True
        if self.zoom > self.zoomRangeMax:
            self.zoom, clamped = self.zoomRangeMax, True

        if not clamped or self.zoomClamped is False:
            self.scale(zoomFactor, zoomFactor)

    def _StartEdgeDrag(self, item: typing.Any) -> typing.Any:

        assert isinstance(item, JGraphicSocket)
        if item.socketType == GRSOCKET_TYPE_INPUT:
            return

        if item.multiConnectionType:
            self.__tempEdgeDragInstance = JGraphicEdge(
                startSocket=item, destinationSocket=None, tempDragPos=item.scenePos()
            )
            self.scene().addItem(self.__tempEdgeDragInstance)
            self.__tempEdgeDragMode = True
            self.__tempSocket = item

        elif not item.multiConnectionType and len(item.edgeList) == 0:
            self.__tempEdgeDragInstance = JGraphicEdge(
                startSocket=item, destinationSocket=None, tempDragPos=item.scenePos()
            )
            self.scene().addItem(self.__tempEdgeDragInstance)
            self.__tempEdgeDragMode = True
            self.__tempSocket = item

    def _EndEdgeDrag(self, item: typing.Any):

        assert isinstance(self.__tempEdgeDragInstance, JGraphicEdge)
        if isinstance(item, JGraphicSocket):

            if self.__tempSocket == item:
                self.__tempEdgeDragInstance.RemoveFromSockets()
                self.scene().removeItem(self.__tempEdgeDragInstance)
                self._ResetEdgeDrag()

            elif self.__tempSocket.socketType == item.socketType:
                self.__tempEdgeDragInstance.RemoveFromSockets()
                self.scene().removeItem(self.__tempEdgeDragInstance)
                self._ResetEdgeDrag()

            else:
                assert isinstance(self.__tempEdgeDragInstance, JGraphicEdge)
                self.__tempEdgeDragInstance.destinationSocket = item
                self._ResetEdgeDrag()

            self.setInteractive(True)

        elif not isinstance(item, JGraphicSocket):
            self.__tempEdgeDragInstance.RemoveFromSockets()
            self.scene().removeItem(self.__tempEdgeDragInstance)
            self._ResetEdgeDrag()
            self.setInteractive(True)

    def _ResetEdgeDrag(self):
        assert isinstance(self.__tempEdgeDragInstance, JGraphicEdge)
        self.__tempEdgeDragMode = False
        self.__tempSocket = None
        self.__tempEdgeDragInstance = None
