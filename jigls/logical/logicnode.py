from __future__ import annotations

import logging
from typing import List, Optional, Union

from jigls.concrete.base import Base
from jigls.concrete.edge import Edge
from jigls.concrete.node import Node

from jigls.logger import logger

logger = logging.getLogger(__name__)


class LogicNode(Node):

    __type__ = "LogicNode"

    def __init__(
        self,
        parent: Base,
        name: str,
        value: Optional[bool] = None,
        dirty: bool = False,
        enable: bool = True,
        debug: bool = False,
    ):
        super().__init__(
            parent, name, dirty=dirty, enable=enable, debug=debug
        )

        self.value: Optional[bool] = value

    def GetValue(self) -> Optional[bool]:
        return self.value

    def SetValue(self, value: Optional[bool]) -> bool:

        if self.value == value:
            return False
        else:
            if self.debug:
                logger.info(
                    f"[P:{self.parent.name}] [N:{self.name}] value change {self.value} - {value}"
                )
            self.value = value
            return True

    def Evaluate(self, value: Optional[bool]):

        if not self.SetValue(value):
            return

        if self.IsEnabled():
            if isinstance(self.parent, Edge):
                if self.debug:
                    logger.debug(
                        f"[N:{self.name}] triggered [P:{self.parent.name}]"
                    )
                self.parent.Evaluate()

            for connection in self.connections:

                if self.debug:
                    logger.debug(
                        f"[P:{self.parent.name}] [N:{self.name}] connection to N:{connection.name} value set {value}"
                    )
                connection.Evaluate(value)