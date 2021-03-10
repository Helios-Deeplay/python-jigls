from __future__ import annotations
from jigls.concrete.base import Base
from jigls.concrete.node import Node


class Edge(Base):

    _type_ = "ConcreteEdge"

    def __init__(
        self,
        name: str,
        dirty: bool = False,
        enable: bool = True,
    ):
        super().__init__(name=name, dirty=dirty, enable=enable)

    def Evaluate(self):
        raise NotImplementedError(
            f"{self.name} edge should implement evaluate function"
        )
