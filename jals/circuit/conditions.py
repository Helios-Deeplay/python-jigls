import operator
from typing import Optional, Union
from jals.circuit.base import Base
from jals.circuit.logicnode import LNode

from jals.circuit.gate import SGate


class SetIF(SGate):
    def __init__(
        self,
        name,
        check: Optional[Union[str, int]],
        setTrue: Optional[Union[str, int]],
        setFalse: Optional[Union[str, int]],
        debug=False,
    ):
        super().__init__(name, debug)
        self.B.value = check
        self.sett: Optional[Union[str, int]] = setTrue
        self.setf: Optional[Union[str, int]] = setFalse

    def evaluate(self):
        if operator.eq(self.A.value, self.B.value):
            self.Q.set(self.sett)
        else:
            self.Q.set(self.setf)
