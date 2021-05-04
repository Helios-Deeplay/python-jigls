from jeditor.core.graphicedge import JGraphicEdge
from jeditor.core.graphicsocket import JGraphicSocket
import typing
from copy import deepcopy

from .constants import (
    GREDGE_PATH_BEZIER,
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
import logging

from jeditor.logger import logger

logger = logging.getLogger(__name__)


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
        self.scrollbarVertPolicy: int = GRVIEW_VERT_SCROLLBAR
        self.scrollbarHorzPolicy: int = GRVIEW_HORZ_SCROLLBAR

        self._zoomInFactor: float = GRVIEW_ZOOM_IN_FACTOR
        self._zoomClamped: bool = GRVIEW_ZOOM_CLAMPED
        self._zoom: int = GRVIEW_ZOOM
        self._zoomStep: int = GRVIEW_ZOOM_STEP

        self._zoomRangeMin = GRVIEW_ZOOM_RANGE_MIN
        self._zoomRangeMax = GRVIEW_ZOOM_RANGE_MAX

        self._rubberband: QtWidgets.QRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self._currentState: int = GRVIEW_OP_MODE_DEFAULT

        self._rubberBandStart: QtCore.QPoint = QtCore.QPoint()
        self.s: QtCore.QPoint = QtCore.QPoint()

        self._tempSocket: typing.Optional[JGraphicSocket] = None
        self._tempEdgeDragMode: bool = False
        self._tempEdgeDragInstance: typing.Optional[JGraphicEdge] = None

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
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy(self.scrollbarHorzPolicy)
        )
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy(self.scrollbarVertPolicy)
        )
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event: QtGui.QMouseEvent):

        # * pan view
        if event.button() == QtCore.Qt.RightButton:
            self._currentState = GRVIEW_OP_MODE_PAN_VIEW
            self.prevPos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self.setInteractive(False)

        # * Rubber band selection
        elif (
            event.button() == QtCore.Qt.LeftButton
            and event.modifiers() == QtCore.Qt.NoModifier
            and self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            is None
        ):
            self._currentState = GRVIEW_OP_MODE_SELECTION
            self._InitRubberband(event.pos())
            self.setInteractive(False)

        # * start edge drag
        elif (
            event.button() == QtCore.Qt.LeftButton
            and self._currentState == GRVIEW_OP_MODE_DEFAULT
            and not self._tempEdgeDragMode
            and isinstance(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()),
                JGraphicSocket,
            )
        ):
            self._currentState = GRVIEW_OP_MODE_EDGE_DRAG
            self.prevPos = event.pos()
            self._StartEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )

        # * end edge drag
        if (
            event.button() == QtCore.Qt.LeftButton
            and self._tempEdgeDragMode
            and self._currentState != GRVIEW_OP_MODE_EDGE_DRAG
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

        # * pan canvas.
        if self._currentState == GRVIEW_OP_MODE_PAN_VIEW:
            offset = self.prevPos - event.pos()  # type:ignore
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + offset.y()
            )
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + offset.x()
            )

        # * RuberBand selection.
        elif self._currentState == GRVIEW_OP_MODE_SELECTION:
            self._rubberband.setGeometry(
                QtCore.QRect(self._rubberBandOrigin, event.pos()).normalized()
            )

        # * Edge drag
        elif self._tempEdgeDragMode:
            self._tempEdgeDragInstance.tempDragPos = self.mapToScene(event.pos())
            self._tempEdgeDragInstance.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):

        # * Drag
        if self._currentState == GRVIEW_OP_MODE_PAN_VIEW:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)

        # * Selection.
        elif self._currentState == GRVIEW_OP_MODE_SELECTION:
            self._rubberband.setGeometry(
                QtCore.QRect(self._rubberBandOrigin, event.pos()).normalized()
            )
            painterPath = self._ReleaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)

        self._currentState = GRVIEW_OP_MODE_DEFAULT

        super().mouseReleaseEvent(event)

    def _InitRubberband(self, position: QtCore.QPoint):
        self._rubberBandStart = position
        self._rubberBandOrigin = position
        self._rubberband.setGeometry(
            QtCore.QRect(self._rubberBandOrigin, QtCore.QSize())
        )
        self._rubberband.show()

    def _ReleaseRubberband(self):
        painterPath = QtGui.QPainterPath()
        rect = self.mapToScene(self._rubberband.geometry())
        painterPath.addPolygon(rect)
        self._rubberband.hide()
        return painterPath

    def wheelEvent(self, event: QtGui.QWheelEvent):
        zoomOutFactor = 1 / self._zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = self._zoomInFactor
            self._zoom += self._zoomStep
        else:
            zoomFactor = zoomOutFactor
            self._zoom -= self._zoomStep

        clamped = False
        if self._zoom < self._zoomRangeMin:
            self._zoom, clamped = self._zoomRangeMin, True
        if self._zoom > self._zoomRangeMax:
            self._zoom, clamped = self._zoomRangeMax, True

        if not clamped or self._zoomClamped is False:
            self.scale(zoomFactor, zoomFactor)

    def _StartEdgeDrag(self, item: typing.Any) -> typing.Any:

        assert isinstance(item, JGraphicSocket)
        if item.socketType == GRSOCKET_TYPE_INPUT:
            return

        if item.multiConnectionType:
            self._tempEdgeDragInstance = JGraphicEdge(
                startSocket=item, destinationSocket=None
            )
            self._tempEdgeDragInstance.tempDragPos = item.scenePos()
            self.scene().addItem(self._tempEdgeDragInstance)
            self._tempEdgeDragMode = True
            self._tempSocket = item
            self.setCursor(QtCore.Qt.DragLinkCursor)

        elif not item.AtMaxEdgeLimit():
            self._tempEdgeDragInstance = JGraphicEdge(
                startSocket=item,
                destinationSocket=None,
                edgePathType=GREDGE_PATH_BEZIER,
            )
            self._tempEdgeDragInstance.tempDragPos = item.scenePos()
            self.scene().addItem(self._tempEdgeDragInstance)
            self._tempEdgeDragMode = True
            self._tempSocket = item
            self.setCursor(QtCore.Qt.DragLinkCursor)

    def _EndEdgeDrag(self, item: typing.Any):

        assert isinstance(self._tempEdgeDragInstance, JGraphicEdge)
        if isinstance(item, JGraphicSocket):

            # * check same socket
            if self._tempSocket is item:
                logger.warning(f"tried connecting same socket")
                self._tempEdgeDragInstance.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragInstance)
                self._ResetEdgeDrag()
            # * check if same socket type, intput type
            elif self._tempSocket.socketType == item.socketType:
                logger.warning(f"tried connecting same socket type")
                self._tempEdgeDragInstance.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragInstance)
                self._ResetEdgeDrag()
            # * check if connecttion possible, non multi connection type
            elif item.AtMaxEdgeLimit():
                logger.warning(f"socket cannot add edge, maxlimit")
                self._tempEdgeDragInstance.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragInstance)
                self._ResetEdgeDrag()
            # * check sockets belong to same parent
            elif self._tempEdgeDragInstance._startSocket.parentNode == item.parentNode:
                logger.warning(f"socket belong to same parent")
                self._tempEdgeDragInstance.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragInstance)
                self._ResetEdgeDrag()
            # * only add edge if all above fail
            else:

                self._tempEdgeDragInstance.destinationSocket = item
                logger.info(
                    f"{self._tempEdgeDragInstance.destinationSocket.socketType} - {len(self._tempEdgeDragInstance.destinationSocket.edgeList)} - {self._tempEdgeDragInstance.destinationSocket.AtMaxEdgeLimit()}"
                )
                self._ResetEdgeDrag()

        elif not isinstance(item, JGraphicSocket):
            logger.warning(f"clicked no socket type")
            self._tempEdgeDragInstance.RemoveFromSockets()
            self.scene().removeItem(self._tempEdgeDragInstance)
            self._ResetEdgeDrag()
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)

    def _ResetEdgeDrag(self):
        assert isinstance(self._tempEdgeDragInstance, JGraphicEdge)
        self._tempEdgeDragMode = False
        self._tempSocket = None
        self._tempEdgeDragInstance = None
        self.setCursor(QtCore.Qt.ArrowCursor)
