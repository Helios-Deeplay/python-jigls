import inspect
import logging

from jals.circuit.gate import LGate
from jals.circuit.logicnode import LNode
from jals.logger import logger

logger = logging.getLogger(__name__)


class Not(LGate):
    def __init__(self, name, debug=False):
        super().__init__(name, debug)
        # self.A = Node(self, "A", activates=True)
        # self.B = None
        # self.Q = LNode(self, "Q")

    def evaluate(self):
        self.Q.set(not self.A.value)


class And(LGate):
    def __init__(self, name, debug=False):
        super().__init__(name, debug)

    def evaluate(self):
        self.Q.set(self.A.value and self.B.value)


class Or(LGate):
    def __init__(self, name, debug=False):
        super().__init__(name, debug)

    def evaluate(self):
        self.Q.set(self.A.value or self.B.value)


class Xor(LGate):
    def __init__(self, name, debug=False):
        super().__init__(name, debug)

        self.and1 = And("XOR_AND_1")
        self.and2 = And("XOR_AND_2")
        self.not1 = Not("XOR_NOT_1")
        self.not2 = Not("XOR_NOT_2")
        self.or1 = Or("XOR_OR_1")

        self.A.connect([self.and1.A, self.not2.A])
        self.B.connect([self.not1.A, self.and2.A])

        self.not1.Q.connect([self.and1.B])
        self.not2.Q.connect([self.and2.B])
        self.and1.Q.connect([self.or1.A])
        self.and2.Q.connect([self.or1.B])
        self.or1.Q.connect([self.Q])


def Bit(x, bit):
    return x[bit] == "1"
