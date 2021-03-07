from __future__ import annotations

from typing import List, Optional, Union
from jals.circuit.base import Base

import inspect
import logging

from jals.logger import logger

logger = logging.getLogger(__name__)


class LNode(Base):

    __type__ = "LogicNode"

    def __init__(
        self,
        parent: Base,
        name: str,
        activates: bool = False,
        enable: bool = False,
        debug: bool = True,
    ):
        super().__init__(name)

        self.value: Optional[int] = None
        self.parent: Base = parent
        self.name: str = name
        self.activates: bool = activates
        self.enable: bool = enable
        self.debug: bool = debug

        self.connects: List[LNode] = []

    def connect(self, connections: Union[List[LNode], LNode]) -> None:
        if not isinstance(connections, list):
            connections = [connections]
        for input in connections:
            self.connects.append(input)

    def set(self, value):
        if self.value == value:
            return

        pvalue = self.value
        self.value = value

        if self.debug:
            logger.debug(
                f"{self.parent.name} {self.name} value change {pvalue} - {self.value}"
            )

        if self.activates:
            if self.debug:
                logger.debug(
                    f"change in {self.name} triggering {self.parent.name}"
                )
            self.parent.evaluate()

        for con in self.connects:
            if self.debug:
                logger.debug(
                    f"connection to {con.name} value set {value} from {self.name}"
                )
            con.set(value)
