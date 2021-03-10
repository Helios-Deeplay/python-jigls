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

    def SetEnable(self):
        raise NotImplementedError(
            f"{self.name} edge should implement SetEnable function"
        )

    def SetValue(self, *args, **kwargs):
        raise NotImplementedError(
            f"{self.name} edge should implement SetValue function"
        )

    def Run(self):
        raise NotImplementedError(
            f"{self.name} edge should implement Run function"
        )

    def Evaluate(self, *args, **kwargs):
        raise NotImplementedError(
            f"{self.name} edge should implement Evaluate function"
        )
