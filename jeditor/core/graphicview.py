from jeditor.core.scenemanager import JSceneManager
from jeditor.core.graphicnode import JGraphicNode
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
        sceneManager: JSceneManager,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._sceneManager: JSceneManager = sceneManager

        self.setScene(sceneManager.graphicsScene)

        self.initUI()

    def initUI(self):

        self.scrollbarVertPolicy: int = GRVIEW_VERT_SCROLLBAR
        self.scrollbarHorzPolicy: int = GRVIEW_HORZ_SCROLLBAR

        self._zoomInFactor: float = GRVIEW_ZOOM_IN_FACTOR
        self._zoomClamped: bool = GRVIEW_ZOOM_CLAMPED
        self._zoom: int = GRVIEW_ZOOM
        self._zoomStep: int = GRVIEW_ZOOM_STEP

        self._zoomRangeMin = GRVIEW_ZOOM_RANGE_MIN
        self._zoomRangeMax = GRVIEW_ZOOM_RANGE_MAX
        self._currentState: int = GRVIEW_OP_MODE_DEFAULT

        self._rubberband: QtWidgets.QRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )

        self._rubberBandStart: QtCore.QPoint = QtCore.QPoint()
        self.s: QtCore.QPoint = QtCore.QPoint()

        self._tempSocket: typing.Optional[JGraphicSocket] = None
        self._tempEdgeDragObj: typing.Optional[JGraphicEdge] = None

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
            and isinstance(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()),
                JGraphicSocket,
            )
        ):
            self._currentState = GRVIEW_OP_MODE_EDGE_DRAG
            self._StartEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )

        # * end edge drag
        elif (
            event.button() == QtCore.Qt.LeftButton
            and self._currentState == GRVIEW_OP_MODE_EDGE_DRAG
        ):
            # logger.debug("pre")
            self._EndEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )
            # logger.debug("post")

        # * debug
        elif event.button() == QtCore.Qt.MidButton:
            logging.debug("---")
            for item in self.scene().items():
                if isinstance(item, (JGraphicEdge, JGraphicNode)):
                    logging.debug(item)

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
        elif self._currentState == GRVIEW_OP_MODE_EDGE_DRAG:
            self._tempEdgeDragObj.tempDragPos = self.mapToScene(event.pos())
            self._tempEdgeDragObj.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):

        # * Pan view
        if self._currentState == GRVIEW_OP_MODE_PAN_VIEW:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)
            self._currentState = GRVIEW_OP_MODE_DEFAULT

        # * Selection.
        elif self._currentState == GRVIEW_OP_MODE_SELECTION:
            self._rubberband.setGeometry(
                QtCore.QRect(self._rubberBandOrigin, event.pos()).normalized()
            )
            painterPath = self._ReleaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)
            self._currentState = GRVIEW_OP_MODE_DEFAULT

        elif self._currentState == GRVIEW_OP_MODE_EDGE_DRAG:
            pass

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:

        if (
            event.button() == QtCore.Qt.LeftButton
            and self._currentState == GRVIEW_OP_MODE_DEFAULT
            and isinstance(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()),
                JGraphicEdge,
            )
        ):

            item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            assert isinstance(item, JGraphicEdge)
            self._currentState = GRVIEW_OP_MODE_EDGE_DRAG
            self._StartEdgeEditing(item, self.mapToScene(event.pos()))

        return super().mouseDoubleClickEvent(event)

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

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Delete:
            self._DeleteItemsFromScene()
        elif (
            event.key() == QtCore.Qt.Key_S
            and event.modifiers() == QtCore.Qt.ControlModifier
        ):
            self._sceneManager.SaveToFile()
        elif (
            event.key() == QtCore.Qt.Key_O
            and event.modifiers() == QtCore.Qt.ControlModifier
        ):
            self._sceneManager.Deserialize(self._sceneManager.LoadFromFile())

        super().keyPressEvent(event)

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

    def _StartEdgeDrag(self, item: typing.Any) -> typing.Any:

        assert isinstance(item, JGraphicSocket)
        if item.socketType == GRSOCKET_TYPE_INPUT:
            self._currentState = GRVIEW_OP_MODE_DEFAULT
            return

        if item.multiConnection:
            self._tempEdgeDragObj = JGraphicEdge(
                startSocket=item,
                destinationSocket=None,
                edgePathType=GREDGE_PATH_BEZIER,
            )
            self._tempEdgeDragObj.tempDragPos = item.scenePos()
            self.scene().addItem(self._tempEdgeDragObj)
            self._tempEdgeDragObj.update()
            self._tempSocket = item
            self.setCursor(QtCore.Qt.DragLinkCursor)

        elif not item.AtMaxEdgeLimit():
            self._tempEdgeDragObj = JGraphicEdge(
                startSocket=item,
                destinationSocket=None,
                edgePathType=GREDGE_PATH_BEZIER,
            )
            self._tempEdgeDragObj.tempDragPos = item.scenePos()
            self.scene().addItem(self._tempEdgeDragObj)
            self._tempSocket = item
            self.setCursor(QtCore.Qt.DragLinkCursor)
        else:
            self._currentState = GRVIEW_OP_MODE_DEFAULT

    def _EndEdgeDrag(self, item: typing.Any):

        assert isinstance(self._tempEdgeDragObj, JGraphicEdge)
        if isinstance(item, JGraphicSocket):

            # * check same socket
            if self._tempSocket is item:
                logger.warning(f"tried connecting same socket")
                self._tempEdgeDragObj.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            # * check if same socket type, intput type
            elif self._tempSocket.socketType == item.socketType:
                logger.warning(f"tried connecting same socket type")
                self._tempEdgeDragObj.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            # * check if connecttion possible, non multi connection type
            elif item.AtMaxEdgeLimit():
                logger.warning(f"socket cannot add edge, maxlimit")
                self._tempEdgeDragObj.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            # * check sockets belong to same parent
            elif self._tempEdgeDragObj.startSocket.parentNodeID == item.parentNodeID:
                logger.warning(f"socket belong to same parent")
                self._tempEdgeDragObj.RemoveFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            else:
                # * check dupliate edge
                for edgeInScene in self.scene().items():
                    if isinstance(edgeInScene, JGraphicEdge):
                        # todo fix this. have to add and edge id ignore the edge when doing this check. should not use `is` keyword which doing this!
                        # * implement edge id
                        if (
                            edgeInScene.startSocket is self._tempEdgeDragObj.startSocket
                            and edgeInScene.destinationSocket is item
                        ):
                            logger.warning(f"duplicate edge")
                            self._tempEdgeDragObj.RemoveFromSockets()
                            self.scene().removeItem(self._tempEdgeDragObj)
                            self._ResetEdgeDrag()
                            return

                # * only add edge if all above fail
                self._tempEdgeDragObj.destinationSocket = item
                self._ResetEdgeDrag()

        elif not isinstance(item, JGraphicSocket):
            logger.warning(f"clicked no socket type")
            self._tempEdgeDragObj.RemoveFromSockets()
            self.scene().removeItem(self._tempEdgeDragObj)
            self._ResetEdgeDrag()
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)

    def _StartEdgeEditing(self, edge: JGraphicEdge, cursor: QtCore.QPointF):
        self._tempEdgeDragObj = edge
        self._tempEdgeDragObj.tempDragPos = cursor
        self._tempSocket = edge.startSocket
        self.setCursor(QtCore.Qt.DragLinkCursor)
        self._tempEdgeDragObj.update()

    def _ResetEdgeDrag(self):
        assert isinstance(self._tempEdgeDragObj, JGraphicEdge)
        self._tempSocket = None
        self._tempEdgeDragObj = None
        self._currentState = GRVIEW_OP_MODE_DEFAULT
        self.setCursor(QtCore.Qt.ArrowCursor)
        # logger.debug("reset")

    def _DeleteItemsFromScene(self):

        edgeList: typing.Set[JGraphicEdge] = set()
        nodeList: typing.Set[JGraphicNode] = set()

        if not self.scene().selectedItems():
            logger.debug("no items selected")
            return

        for item in self.scene().selectedItems():
            if isinstance(item, JGraphicNode):
                for socket in item.socketManager.socketList:
                    for edge in socket.edgeList:
                        assert isinstance(edge, JGraphicEdge)
                        edgeList.add(edge)
                nodeList.add(item)
            elif isinstance(item, JGraphicEdge):
                edgeList.add(item)
            else:
                logger.error("unknown item in delete selection")

        for edge in edgeList:
            self._DeleteEdgeFromScene(edge)
        for node in nodeList:
            self._DeleteNodeFromScene(node)

    def _DeleteEdgeFromScene(self, edge: JGraphicEdge):
        assert isinstance(edge, JGraphicEdge)
        assert edge in self.scene().items()
        edge.RemoveFromSockets()
        self.scene().removeItem(edge)

    def _DeleteNodeFromScene(self, node: JGraphicNode):
        assert isinstance(node, JGraphicNode)
        assert node in self.scene().items()
        self.scene().removeItem(node)
