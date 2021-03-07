from dataclasses import dataclass, field
from typing import List, NamedTuple, Optional, Tuple

EdgePair = NamedTuple('EdgePair', [('start', str), ('end', str)])

LaneLinkData = NamedTuple('LaneLinkData', [('predLaneId', str), ('LaneId', str), ('succLaneId', str)])

@dataclass
class EdgeLink:

    _start: str
    _end: str
    _label: str
    _color: str
    _traversed: int = 0

    @property
    def key(self)->EdgePair:
        return EdgePair(self._start, self._end)

    @key.setter
    def key(self, pair: EdgePair) -> None:
        self._start = pair.start
        self._end = pair.end
        self._label = f"{self._start}_{self._end}"

    @property
    def start(self)->Optional[str]:
        return self._start

    @property
    def end(self)->Optional[str]:
        return self._end

    @property
    def label(self)->Optional[str]:
        return self._label

    @label.setter
    def label(self, value: str)->None:
        self._label = value

    @property
    def color(self)->Optional[str]:
        return self._color

    @color.setter
    def color(self, value:str)->None:
        self._color = value

    @property
    def traversed(self)->int:
        return self._traversed

    def IncTraversed(self):
        self._traversed += 1


@dataclass
class Node:
    _node: str
    _road: str
    _section: str
    _lane: str
    _traversed: int = 0

    @property
    def node(self):
        return self._node
    
    @node.setter
    def node(self, value:str)->None:
        self._node = value
        # print(f"! direct assingment not allowed.")
    
    @property
    def road(self):
        return self._road

    @property
    def section(self):
        return self._section

    @property
    def lane(self):
        return self._lane

    @property
    def traversed(self)->int:
        return self._traversed

    def IncTraversed(self):
        self._traversed += 1
