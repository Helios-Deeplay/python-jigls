from jals.circuit.logicnode import LNode
from jals.circuit.statenode import SNode

from jals.circuit.base import Base


class LGate(Base):
    """
    operators should have input and outputs defined.
    """

    __slots__ = ["A", "B", "Q"]

    def __init__(self, name, debug):
        super().__init__(name)

        self.A = LNode(
            self, "_".join(("in_A", name)), activates=True, debug=debug
        )

        self.B = LNode(
            self, "_".join(("in_B", name)), activates=True, debug=debug
        )

        self.Q = LNode(self, "_".join(("out_Q", name)), debug=debug)


class SGate(Base):
    """
    operators should have input and outputs defined.
    """

    __slots__ = ["A", "B", "Q"]

    def __init__(self, name, debug):
        super().__init__(name)

        self.A = SNode(
            self, "_".join(("in_A", name)), activates=True, debug=debug
        )

        self.B = SNode(
            self, "_".join(("in_B", name)), activates=True, debug=debug
        )

        self.Q = SNode(self, "_".join(("out_Q", name)), debug=debug)
