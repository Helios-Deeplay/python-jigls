from jeditor.core import graphicscene
from jeditor.core.commands import EdgeRemoveCommand, NodeRemoveCommand
import logging
import typing
from copy import deepcopy

from jeditor.core.graphicedge import JGraphicEdge
from jeditor.core.graphicnode import JGraphicNode
from jeditor.core.graphicsocket import JGraphicSocket
from jeditor.core.scenemanager import JSceneManager
from jeditor.logger import logger
from PyQt5 import QtCore, QtGui, QtWidgets

from .constants import JCONSTANTS

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

        self.scrollbarVertPolicy: int = JCONSTANTS.GRVIEW.VERT_SCROLLBAR
        self.scrollbarHorzPolicy: int = JCONSTANTS.GRVIEW.HORZ_SCROLLBAR

        self._zoomInFactor: float = JCONSTANTS.GRVIEW.ZOOM_IN_FACTOR
        self._zoomClamped: bool = JCONSTANTS.GRVIEW.ZOOM_CLAMPED
        self._zoom: int = JCONSTANTS.GRVIEW.ZOOM
        self._zoomStep: int = JCONSTANTS.GRVIEW.ZOOM_STEP

        self._zoomRangeMin = JCONSTANTS.GRVIEW.ZOOM_RANGE_MIN
        self._zoomRangeMax = JCONSTANTS.GRVIEW.ZOOM_RANGE_MAX
        self._currentState: int = JCONSTANTS.GRVIEW.OP_MODE_DEFAULT

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
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_PAN_VIEW
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
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_SELECTION
            self._InitRubberband(event.pos())
            self.setInteractive(False)

        # * start edge drag
        elif (
            event.button() == QtCore.Qt.LeftButton
            and self._currentState == JCONSTANTS.GRVIEW.OP_MODE_DEFAULT
            and isinstance(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()),
                JGraphicSocket,
            )
        ):
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_EDGE_DRAG
            self._StartEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )

        # * end edge drag
        elif (
            event.button() == QtCore.Qt.LeftButton
            and self._currentState == JCONSTANTS.GRVIEW.OP_MODE_EDGE_DRAG
        ):
            self._EndEdgeDrag(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            )

        # * debug
        elif event.button() == QtCore.Qt.MidButton:
            logger.debug("items in scene")
            for item in self.scene().items():
                if isinstance(item, (JGraphicEdge, JGraphicNode, JGraphicSocket)):
                    logger.debug(item)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):

        # * pan canvas.
        if self._currentState == JCONSTANTS.GRVIEW.OP_MODE_PAN_VIEW:
            offset = self.prevPos - event.pos()  # type:ignore
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + offset.y()
            )
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + offset.x()
            )

        # * RuberBand selection.
        elif self._currentState == JCONSTANTS.GRVIEW.OP_MODE_SELECTION:
            self._rubberband.setGeometry(
                QtCore.QRect(self._rubberBandOrigin, event.pos()).normalized()
            )

        # * Edge drag
        elif self._currentState == JCONSTANTS.GRVIEW.OP_MODE_EDGE_DRAG:
            self._tempEdgeDragObj.DragPos = self.mapToScene(event.pos())
            self._tempEdgeDragObj.update()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):

        # * Pan view
        if self._currentState == JCONSTANTS.GRVIEW.OP_MODE_PAN_VIEW:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_DEFAULT

        # * Selection.
        elif self._currentState == JCONSTANTS.GRVIEW.OP_MODE_SELECTION:
            self._rubberband.setGeometry(
                QtCore.QRect(self._rubberBandOrigin, event.pos()).normalized()
            )
            painterPath = self._ReleaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_DEFAULT

        elif self._currentState == JCONSTANTS.GRVIEW.OP_MODE_EDGE_DRAG:
            pass

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:

        if (
            event.button() == QtCore.Qt.LeftButton
            and self._currentState == JCONSTANTS.GRVIEW.OP_MODE_DEFAULT
            and isinstance(
                self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform()),
                JGraphicEdge,
            )
        ):

            item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            assert isinstance(item, JGraphicEdge)
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_EDGE_DRAG
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
            self._RemoveFromScene()
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
        elif (
            event.key() == QtCore.Qt.Key_Z
            and event.modifiers() == QtCore.Qt.ControlModifier
        ):
            self._sceneManager.undoStack.undo()
        elif (
            event.key() == QtCore.Qt.Key_R
            and event.modifiers() == QtCore.Qt.ControlModifier
        ):
            self._sceneManager.undoStack.redo()

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
        if item.socketType == JCONSTANTS.GRSOCKET.TYPE_INPUT:
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_DEFAULT
            return

        if item.multiConnection:
            self._tempEdgeDragObj = JGraphicEdge.DragNewEdge(
                startSocket=item,
                dragPos=item.scenePos(),
            )
            self.scene().addItem(self._tempEdgeDragObj)
            self._tempEdgeDragObj.update()
            self._tempSocket = item
            self.setCursor(QtCore.Qt.DragLinkCursor)

        elif not item.AtMaxLimit():
            self._tempEdgeDragObj = JGraphicEdge.DragNewEdge(
                startSocket=item,
                dragPos=item.scenePos(),
            )
            self.scene().addItem(self._tempEdgeDragObj)
            self._tempEdgeDragObj.update()
            self._tempSocket = item
            self.setCursor(QtCore.Qt.DragLinkCursor)
        else:
            self._currentState = JCONSTANTS.GRVIEW.OP_MODE_DEFAULT

    def _EndEdgeDrag(self, item: typing.Any):

        assert isinstance(self._tempEdgeDragObj, JGraphicEdge)
        if isinstance(item, JGraphicSocket):

            # * check same socket
            if self._tempSocket.socketId == item.socketId:
                logger.warning(f"tried connecting same socket")
                self._tempEdgeDragObj.DisconnectFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            # * check if same socket type, intput type
            elif self._tempSocket.socketType == item.socketType:
                logger.warning(f"tried connecting same socket type")
                self._tempEdgeDragObj.DisconnectFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            # * check if connecttion possible, non multi connection type
            elif item.AtMaxLimit():
                logger.warning(f"socket cannot add edge, maxlimit")
                self._tempEdgeDragObj.DisconnectFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            # * check sockets belong to same parent
            elif self._tempEdgeDragObj.startSocket.nodeId == item.nodeId:
                logger.warning(f"socket belong to same parent")
                self._tempEdgeDragObj.DisconnectFromSockets()
                self.scene().removeItem(self._tempEdgeDragObj)
                self._ResetEdgeDrag()

            else:
                # * check dupliate edge
                for edgeInScene in list(
                    filter(
                        lambda edge: isinstance(edge, JGraphicEdge)
                        and edge.edgeId != self._tempEdgeDragObj.edgeId
                        and edge.startSocket.socketId
                        == self._tempEdgeDragObj.startSocket.socketId,
                        self.scene().items(),
                    )
                ):
                    assert isinstance(edgeInScene, JGraphicEdge)
                    if edgeInScene.destinationSocket is item:
                        logger.warning(f"duplicate edge")
                        self._tempEdgeDragObj.DisconnectFromSockets()
                        self.scene().removeItem(self._tempEdgeDragObj)
                        self._ResetEdgeDrag()
                        return

                # * only add edge if all above fail
                self._tempEdgeDragObj.destinationSocket = item
                self._ResetEdgeDrag()

        elif not isinstance(item, JGraphicSocket):
            logger.warning(f"clicked no socket type")
            self._tempEdgeDragObj.DisconnectFromSockets()
            self.scene().removeItem(self._tempEdgeDragObj)
            self._ResetEdgeDrag()
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)

    def _StartEdgeEditing(self, edge: JGraphicEdge, cursor: QtCore.QPointF):
        self._tempEdgeDragObj = edge
        self._tempEdgeDragObj.DragPos = cursor
        self._tempSocket = edge.startSocket
        self.setCursor(QtCore.Qt.DragLinkCursor)
        self._tempEdgeDragObj.update()

    def _ResetEdgeDrag(self):
        assert isinstance(self._tempEdgeDragObj, JGraphicEdge)
        self._tempSocket = None
        self._tempEdgeDragObj = None
        self._currentState = JCONSTANTS.GRVIEW.OP_MODE_DEFAULT
        self.setCursor(QtCore.Qt.ArrowCursor)
        # logger.debug("reset")

    def _RemoveFromScene(self):

        if not self.scene().selectedItems():
            logger.debug("no items to delete")
            return

        edgeIdRemove: typing.Set[str] = set()
        nodeIdRemove: typing.Set[str] = set()

        for item in self.scene().selectedItems():
            if isinstance(item, JGraphicNode):
                nodeIdRemove.add(item.nodeId)
                for socket in item.socketManager.socketList:
                    edgeIdRemove |= set(socket.edgeList)
            elif isinstance(item, JGraphicEdge):
                edgeIdRemove.add(item.edgeId)
            else:
                logger.debug(f"unknown item selected in delete type {type(item)}")

        logger.debug(f"nodes marked for removal {nodeIdRemove}")
        logger.debug(f"edges marked for removal {edgeIdRemove}")

        self._sceneManager.undoStack.beginMacro("remove item")
        # * first always remove edges, easier to implement undo stack!
        self._RemoveEdgesFromScene(edgeIdRemove)
        self._RemoveNodesFromScene(nodeIdRemove)
        self._sceneManager.undoStack.endMacro()

    def _RemoveNodesFromScene(self, nodes: typing.Set[str]):
        for node in nodes:
            self._RemoveNodeFromScene(node)

    def _RemoveEdgesFromScene(self, edges: typing.Set[str]):
        for edge in edges:
            self._RemoveEdgeFromScene(edge)

    def _RemoveNodeFromScene(self, nodeId: str):
        node_ = list(
            filter(
                lambda node: isinstance(node, JGraphicNode) and node.nodeId == nodeId,
                self.scene().items(),
            )
        )
        assert len(node_) == 1, logger.error(
            f"error fetching node {nodeId} for removal"
        )

        node__ = node_[0]
        assert isinstance(node__, JGraphicNode)
        self.scene().removeItem(node__)

        logger.debug(f"remove node {nodeId}")
        self._sceneManager.undoStack.beginMacro("remove node")
        self._sceneManager.undoStack.push(
            NodeRemoveCommand(
                graphicScene=self._sceneManager.graphicsScene, node=node__
            )
        )
        self._sceneManager.undoStack.endMacro()

    def _RemoveEdgeFromScene(self, edgeId: str):
        edge_ = list(
            filter(
                lambda edge: isinstance(edge, JGraphicEdge) and edge.edgeId == edgeId,
                self.scene().items(),
            )
        )
        assert len(edge_) == 1, logger.error(
            f"error fetching node {edgeId} for removal"
        )

        edge__ = edge_[0]
        assert isinstance(edge__, JGraphicEdge)

        edge__.DisconnectFromSockets()

        logger.debug(f"remove edge {edgeId}")
        self.scene().removeItem(edge__)

        self._sceneManager.undoStack.beginMacro("remove edge")
        self._sceneManager.undoStack.push(
            EdgeRemoveCommand(
                graphicScene=self._sceneManager.graphicsScene, edge=edge__
            )
        )
        self._sceneManager.undoStack.endMacro()
