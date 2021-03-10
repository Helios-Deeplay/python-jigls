from __future__ import annotations

import logging
from typing import List, Optional, Union

from jils.concrete.base import Base
from jils.concrete.edge import Edge
from jils.concrete.node import Node

from jils.logger import logger

logger = logging.getLogger(__name__)


class StateNode(Node):

    __type__ = "StateNode"

    def __init__(
        self,
        parent: Base,
        name: str,
        value: Optional[Union[str, int, float, bool]] = None,
        dirty: bool = False,
        enable: bool = True,
        debug: bool = True,
    ):
        super().__init__(
            parent, name, dirty=dirty, enable=enable, debug=debug
        )

        self.value: Optional[Union[str, int, float, bool]] = value

    def GetValue(self) -> Optional[Union[str, int, float, bool]]:
        return self.value

    def SetValue(
        self, value: Optional[Union[str, int, float, bool]]
    ) -> bool:
        if self.value == value:
            return False
        else:
            self.value = value
            if self.debug:
                logger.info(
                    f"[P:{self.parent.name}] [N:{self.name}] value set to {value}"
                )
            return True

    def Evaluate(self, value: Optional[Union[str, int, float, bool]]):

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
