import typing
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui


class JiglsGraphicView(QtWidgets.QGraphicsView):
    def __init__(
        self,
        grScene,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.grScene = grScene

        self.initUI()
        self.setScene(self.grScene)

        self.zoomInFactor = 1.25
        self.zoomClamped = False
        self.zoom = 10
        self.zoomStep = 1

        # ! implement using namedtuple please
        self.zoomRange = [0, 10]

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

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse
        )

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """Dispatch Qt's mousePress event to corresponding function below"""
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Dispatch Qt's mouseRelease event to corresponding function below"""
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event: QtGui.QMouseEvent):
        releaseEvent = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            event.localPos(),
            event.screenPos(),
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoButton,
            event.modifiers(),
        )
        super().mouseReleaseEvent(releaseEvent)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        fakeEvent = QtGui.QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            QtCore.Qt.LeftButton,
            event.buttons() | QtCore.Qt.LeftButton,  # type:ignore
            event.modifiers(),
        )

        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event: QtGui.QMouseEvent):
        fakeEvent = QtGui.QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            QtCore.Qt.LeftButton,
            event.buttons() & ~QtCore.Qt.LeftButton,  # type:ignore
            event.modifiers(),
        )
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event: QtGui.QMouseEvent):
        return super().mousePressEvent(event)

    def rightMouseButtonPress(self, event: QtGui.QMouseEvent):
        return super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event: QtGui.QMouseEvent):
        return super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event: QtGui.QMouseEvent):
        return super().mousePressEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        zoomOutFactor = 1 / self.zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        if not clamped or self.zoomClamped is False:
            self.scale(zoomFactor, zoomFactor)
