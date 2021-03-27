import sys

from PyQt5.QtWidgets import QApplication

from jiglsgui.editorwindow import NodeEditorWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = NodeEditorWindow()
    wnd.show()

    try:
        app.exec_()
    except Exception as e:
        print(e)
