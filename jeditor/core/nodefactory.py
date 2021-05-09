from typing import Optional
from jeditor.core.constants import GRSOCKET_TYPE_INPUT, GRSOCKET_TYPE_OUTPUT
from jeditor.core.contentwidget import JNodeContent
from jeditor.core.graphicnode import JGraphicNode
import uuid


class JNodeFactory:
    def __init__(self) -> None:
        pass

    def RegisterNode(self):
        pass

    def CreateNode(
        self,
        identifier: Optional[str],
        inputMulti,
        outputMulti,
        inputs=1,
        output=1,
        *args,
        **kwargs
    ):
        if identifier is None:
            identifier = uuid.uuid4().hex
            print(identifier)
        node = JGraphicNode(nodeContent=JNodeContent(), identifier=identifier)
        for _ in range(inputs):
            node.socketManager.AddSocket(
                type=GRSOCKET_TYPE_INPUT, multiConnection=inputMulti
            )
        for _ in range(output):
            node.socketManager.AddSocket(
                type=GRSOCKET_TYPE_OUTPUT, multiConnection=outputMulti
            )

        return node
