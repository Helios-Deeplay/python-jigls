from PyQt5 import QtWidgets


class NodeAddCommand(QtWidgets.QUndoCommand):
    pass


class NodeDeleteCommand(QtWidgets.QUndoCommand):
    pass


class EdgeAddCommand(QtWidgets.QUndoCommand):
    pass


class EdgeDeleteCommand(QtWidgets.QUndoCommand):
    pass


class NodeMoveCommand(QtWidgets.QUndoCommand):
    pass