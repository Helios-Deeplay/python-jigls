import typing

from .constants import (
    GRVIEW_HORZ_SCROLLBAR,
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
        graphicsScene: QtWidgets.QGraphicsScene,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._graphicsScene = graphicsScene

        self.setScene(self._graphicsScene)

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

        # * reference from nodz
        self.rubberband: QtWidgets.QRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self.currentState: str = "DEFAULT"

        self.rubberBandStart: QtCore.QPoint = QtCore.QPoint()
        self.origin: QtCore.QPoint = QtCore.QPoint()

    def initUI(self):

        self.setRenderHints(
            QtGui.QPainter.Antialiasing  # type:ignore
            | QtGui.QPainter.HighQualityAntialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
        )

        self.setViewportUpdateMode(
            QtWidgets.QGraphicsView.FullViewportUpdate
        )

        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy(self.scrollbarHorz)
        )

        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy(self.scrollbarVert)
        )

        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse
        )

    # ! nodz guide
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        # Drag view
        if event.button() == QtCore.Qt.MiddleButton:
            self.currentState = "DRAG_VIEW"
            self.prevPos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self.setInteractive(False)

        # Rubber band selection
        elif (
            event.button() == QtCore.Qt.LeftButton
            and event.modifiers() == QtCore.Qt.NoModifier
            and self.scene().itemAt(
                self.mapToScene(event.pos()), QtGui.QTransform()
            )
            is None
        ):
            self.currentState = "SELECTION"
            self._initRubberband(event.pos())
            self.setInteractive(False)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):

        # Drag canvas.
        if self.currentState == "DRAG_VIEW":
            offset = self.prevPos - event.pos()  # type:ignore
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + offset.y()
            )
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + offset.x()
            )

        # RuberBand selection.
        elif self.currentState == "SELECTION":
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized()
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):

        # Drag
        if self.currentState == "DRAG_VIEW":
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)

        # Selection.
        elif self.currentState == "SELECTION":
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized()
            )
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)

        self.currentState = "DEFAULT"

        super().mouseReleaseEvent(event)

    def _initRubberband(self, position: QtCore.QPoint):
        self.rubberBandStart = position
        self.origin = position
        self.rubberband.setGeometry(
            QtCore.QRect(self.origin, QtCore.QSize())
        )
        self.rubberband.show()

    def _releaseRubberband(self):
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


def NODZGUIDE():
    """
    # # ! nodz guide
    # def mousePressEvent(self, event: QtGui.QMouseEvent):
    #     # Tablet zoom
    #     if (
    #         event.button() == QtCore.Qt.RightButton
    #         and event.modifiers() == QtCore.Qt.AltModifier
    #     ):
    #         self.currentState = "ZOOM_VIEW"
    #         self.initMousePos = event.pos()
    #         self.zoomInitialPos = event.pos()
    #         self.initMouse = QtGui.QCursor.pos()
    #         self.setInteractive(False)

    #     # Drag view
    #     elif (
    #         event.button() == QtCore.Qt.MiddleButton
    #         and event.modifiers() == QtCore.Qt.AltModifier
    #     ):
    #         self.currentState = "DRAG_VIEW"
    #         self.prevPos = event.pos()
    #         self.setCursor(QtCore.Qt.ClosedHandCursor)
    #         self.setInteractive(False)

    #     # Rubber band selection
    #     elif (
    #         event.button() == QtCore.Qt.LeftButton
    #         and event.modifiers() == QtCore.Qt.NoModifier
    #         and self.scene().itemAt(
    #             self.mapToScene(event.pos()), QtGui.QTransform()
    #         )
    #         is None
    #     ):
    #         self.currentState = "SELECTION"
    #         self._initRubberband(event.pos())
    #         self.setInteractive(False)

    #     # Drag Item
    #     elif (
    #         event.button() == QtCore.Qt.LeftButton
    #         and event.modifiers() == QtCore.Qt.NoModifier
    #         and self.scene().itemAt(
    #             self.mapToScene(event.pos()), QtGui.QTransform()
    #         )
    #         is not None
    #     ):
    #         self.currentState = "DRAG_ITEM"
    #         self.setInteractive(True)

    #     # Add selection
    #     elif (
    #         event.button() == QtCore.Qt.LeftButton
    #         and QtCore.Qt.Key_Shift in self.pressedKeys
    #         and QtCore.Qt.Key_Control in self.pressedKeys
    #     ):
    #         self.currentState = "ADD_SELECTION"
    #         self._initRubberband(event.pos())
    #         self.setInteractive(False)

    #     # Subtract selection
    #     elif (
    #         event.button() == QtCore.Qt.LeftButton
    #         and event.modifiers() == QtCore.Qt.ControlModifier
    #     ):
    #         self.currentState = "SUBTRACT_SELECTION"
    #         self._initRubberband(event.pos())
    #         self.setInteractive(False)

    #     # Toggle selection
    #     elif (
    #         event.button() == QtCore.Qt.LeftButton
    #         and event.modifiers() == QtCore.Qt.ShiftModifier
    #     ):
    #         self.currentState = "TOGGLE_SELECTION"
    #         self._initRubberband(event.pos())
    #         self.setInteractive(False)

    #     else:
    #         self.currentState = "DEFAULT"

    #     super().mousePressEvent(event)

    # def mouseMoveEvent(self, event: QtGui.QMouseEvent):
    #     # Zoom.
    #     if self.currentState == "ZOOM_VIEW":
    #         offset = self.zoomInitialPos.x() - event.pos().x()

    #         if offset > self.previousMouseOffset:
    #             self.previousMouseOffset = offset
    #             self.zoomDirection = -1
    #             self.zoomIncr -= 1

    #         elif offset == self.previousMouseOffset:
    #             self.previousMouseOffset = offset
    #             if self.zoomDirection == -1:
    #                 self.zoomDirection = -1
    #             else:
    #                 self.zoomDirection = 1

    #         else:
    #             self.previousMouseOffset = offset
    #             self.zoomDirection = 1
    #             self.zoomIncr += 1

    #         if self.zoomDirection == 1:
    #             zoomFactor = 1.03
    #         else:
    #             zoomFactor = 1 / 1.03

    #         # Perform zoom and re-center on initial click position.
    #         pBefore = self.mapToScene(self.initMousePos)
    #         self.setTransformationAnchor(
    #             QtWidgets.QGraphicsView.AnchorViewCenter
    #         )
    #         self.scale(zoomFactor, zoomFactor)
    #         pAfter = self.mapToScene(self.initMousePos)
    #         diff = pAfter - pBefore

    #         self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
    #         self.translate(diff.x(), diff.y())

    #     # Drag canvas.
    #     elif self.currentState == "DRAG_VIEW":
    #         offset = self.prevPos - event.pos()
    #         self.prevPos = event.pos()
    #         self.verticalScrollBar().setValue(
    #             self.verticalScrollBar().value() + offset.y()
    #         )
    #         self.horizontalScrollBar().setValue(
    #             self.horizontalScrollBar().value() + offset.x()
    #         )

    #     # RuberBand selection.
    #     elif (
    #         self.currentState == "SELECTION"
    #         or self.currentState == "ADD_SELECTION"
    #         or self.currentState == "SUBTRACT_SELECTION"
    #         or self.currentState == "TOGGLE_SELECTION"
    #     ):
    #         self.rubberband.setGeometry(
    #             QtCore.QRect(self.origin, event.pos()).normalized()
    #         )

    #     super().mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
    #     # Zoom the View.
    #     if self.currentState == ".ZOOM_VIEW":
    #         self.offset = 0
    #         self.zoomDirection = 0
    #         self.zoomIncr = 0
    #         self.setInteractive(True)

    #     # Drag View.
    #     elif self.currentState == "DRAG_VIEW":
    #         self.setCursor(QtCore.Qt.ArrowCursor)
    #         self.setInteractive(True)

    #     # Selection.
    #     elif self.currentState == "SELECTION":
    #         self.rubberband.setGeometry(
    #             QtCore.QRect(self.origin, event.pos()).normalized()
    #         )
    #         painterPath = self._releaseRubberband()
    #         self.setInteractive(True)
    #         self.scene().setSelectionArea(painterPath)

    #     # Add Selection.
    #     elif self.currentState == "ADD_SELECTION":
    #         self.rubberband.setGeometry(
    #             QtCore.QRect(self.origin, event.pos()).normalized()
    #         )
    #         painterPath = self._releaseRubberband()
    #         self.setInteractive(True)
    #         for item in self.scene().items(painterPath):
    #             item.setSelected(True)

    #     # Subtract Selection.
    #     elif self.currentState == "SUBTRACT_SELECTION":
    #         self.rubberband.setGeometry(
    #             QtCore.QRect(self.origin, event.pos()).normalized()
    #         )
    #         painterPath = self._releaseRubberband()
    #         self.setInteractive(True)
    #         for item in self.scene().items(painterPath):
    #             item.setSelected(False)

    #     # Toggle Selection
    #     elif self.currentState == "TOGGLE_SELECTION":
    #         self.rubberband.setGeometry(
    #             QtCore.QRect(self.origin, event.pos()).normalized()
    #         )
    #         painterPath = self._releaseRubberband()
    #         self.setInteractive(True)
    #         for item in self.scene().items(painterPath):
    #             if item.isSelected():
    #                 item.setSelected(False)
    #             else:
    #                 item.setSelected(True)

    #     self.currentState = "DEFAULT"

    #     super().mouseReleaseEvent(event)

    # def _initRubberband(self, position: QtCore.QPoint):
    #     self.rubberBandStart = position
    #     self.origin = position
    #     self.rubberband.setGeometry(
    #         QtCore.QRect(self.origin, QtCore.QSize())
    #     )
    #     self.rubberband.show()

    # def _releaseRubberband(self):
    #     painterPath = QtGui.QPainterPath()
    #     rect = self.mapToScene(self.rubberband.geometry())
    #     painterPath.addPolygon(rect)
    #     self.rubberband.hide()
    #     return painterPath
    """
    pass
