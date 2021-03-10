from jils.concrete.edge import Edge
from jils.logical.logicnode import LogicNode


class Not(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str, debug: bool = False):
        super().__init__(
            name,
        )
        self.A = LogicNode(self, "_".join(("in_A", name)), debug=debug)
        self.Q = LogicNode(self, "_".join(("out_Q", name)), debug=debug)

    def Evaluate(self):
        self.Q.Evaluate(not self.A.value)


class And(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str, debug: bool = False):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)), debug=debug)
        self.B = LogicNode(self, "_".join(("in_B", name)), debug=debug)
        self.Q = LogicNode(self, "_".join(("out_Q", name)), debug=debug)

    def Evaluate(self):
        self.Q.Evaluate(self.A.value and self.B.value)


class Or(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str, debug: bool = False):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)), debug=debug)
        self.B = LogicNode(self, "_".join(("in_B", name)), debug=debug)
        self.Q = LogicNode(self, "_".join(("out_Q", name)), debug=debug)

    def Evaluate(self):
        self.Q.Evaluate(self.A.value or self.B.value)


class Xor(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str, debug: bool = False):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)), debug=debug)
        self.B = LogicNode(self, "_".join(("in_B", name)), debug=debug)
        self.Q = LogicNode(self, "_".join(("out_Q", name)), debug=debug)

        self.and1 = And("XOR_AND_1", debug=debug)
        self.and2 = And("XOR_AND_2", debug=debug)
        self.not1 = Not("XOR_NOT_1", debug=debug)
        self.not2 = Not("XOR_NOT_2", debug=debug)
        self.or1 = Or("XOR_OR_1", debug=debug)

        self.A.AddConnection([self.and1.A, self.not2.A])
        self.B.AddConnection([self.not1.A, self.and2.A])

        self.not1.Q.AddConnection([self.and1.B])
        self.not2.Q.AddConnection([self.and2.B])
        self.and1.Q.AddConnection([self.or1.A])
        self.and2.Q.AddConnection([self.or1.B])
        self.or1.Q.AddConnection([self.Q])

    def Evaluate(self):
        pass


def Bit(x, bit):
    return x[bit] == "1"
