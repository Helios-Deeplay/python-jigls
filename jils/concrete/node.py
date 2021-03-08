from __future__ import annotations
from typing import Any, List, Union

from jils.concrete.base import Base


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

        self.connections: List[Node] = []
        self.parent = parent
        self.value: Any = None
        self.debug = debug

    @property
    def type(self):
        return self._type_

    def Connect(self, connections: Union[List[Node], Node]) -> None:
        if not isinstance(connections, list):
            connections = [connections]
        for input in connections:
            self.connections.append(input)

    def setDirty(self, dirty: bool):
        self.dirty = dirty
        if dirty:
            self.parent.dirty = True
            for connection in self.connections:
                connection.setDirty(True)
        else:
            self.parent.dirty = False
            for connection in self.connections:
                connection.setDirty(False)

    def Set(self, *args, **kwargs) -> bool:
        raise NotImplementedError(
            f"{self.name} node must implement a set method"
        )