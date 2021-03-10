from __future__ import annotations

import logging
from typing import Any, List, Optional, Union

from jigls.concrete.base import Base
from jigls.logger import logger

logger = logging.getLogger(__name__)


class Node(Base):

    _type_ = "ConcreteNode"

    def __init__(
        self,
        parent: Base,
        name: str,
        dirty: bool = False,
        enable: bool = True,
        debug: bool = False,
    ):
        super().__init__(name=name, dirty=dirty, enable=enable)

        self.parent = parent
        self.debug = debug
        self.connections: List[Node] = []

    @property
    def type(self):
        return self._type_

    def SetDebug(self, flag: bool):
        self.debug = flag

    def AddConnection(self, connections: Union[List[Node], Node]) -> None:
        if isinstance(connections, list):
            for connection in connections:
                if self.debug:
                    logger.info(
                        f"[P:{self.parent.name}] [N:{self.name}] adding connection [C:{connection.name}]"
                    )
                self.connections.append(connection)
        elif isinstance(connections, Node):
            if self.debug:
                logger.info(
                    f"[P:{self.parent.name}] [N:{self.name}] adding connection [C:{connections.name}]"
                )
            self.connections.append(connections)
        else:
            if self.debug:
                logger.warning(
                    f"[P:{self.parent.name}] [N:{self.name}] failed adding uknown connection type"
                )

    def RemoveConnection(self, connectionname: str) -> bool:
        flag = False
        for connection in self.connections:
            if connection.name == connectionname:
                self.connections.remove(connection)
                if not flag:
                    flag = True

        if flag:
            if self.debug:
                logger.info(
                    f"[P:{self.parent.name}] [N:{self.name}] remove connection [C:{connectionname}]"
                )
            return flag
        else:
            if self.debug:
                logger.info(
                    f"[P:{self.parent.name}] [N:{self.name}] no connection [C:{connectionname}] in list"
                )
            return flag

    def ClearConnect(self) -> None:
        if self.debug:
            logger.info(
                f"[P:{self.parent.name}] [N:{self.name}] connections cleared"
            )
        self.connections.clear()

    def SetDirty(self, flag: bool):
        if self.debug:
            logger.info(
                f"[P:{self.parent.name}] [N:{self.name}] dirty {flag}"
            )
        self.dirty = flag
        for connection in self.connections:
            if self.debug:
                logger.info(
                    f"[P:{self.parent.name}] [N:{self.name}] setting N:[{connection.name}] dirty {flag}"
                )
            connection.SetDirty(flag)

    def SetEnable(self, flag=bool):
        if self.debug:
            logger.info(
                f"[P:{self.parent.name}] [N:{self.name}] enable {flag}"
            )
        self.enable = flag

    def GetValue(self, *args, **kwargs):
        raise NotImplementedError(
            f"{self.name} node must implement a get value method"
        )

    def SetValue(self, *args, **kwargs) -> bool:
        raise NotImplementedError(
            f"{self.name} node must implement a set value method"
        )

    def Evaluate(self, *args, **kwargs):
        raise NotImplementedError(
            f"{self.name} node must implement a evaluate method"
        )
