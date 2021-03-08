from jils.concrete.edge import Edge
from jils.logical.logicnode import LogicNode


class Not(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)))
        self.Q = LogicNode(self, "_".join(("out_Q", name)), enable=False)

    def Evaluate(self):
        self.Q.Set(not self.A.value)


class And(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)))
        self.B = LogicNode(self, "_".join(("in_B", name)))
        self.Q = LogicNode(self, "_".join(("out_Q", name)), enable=False)

    def Evaluate(self):
        self.Q.Set(self.A.value and self.B.value)


class Or(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)))
        self.B = LogicNode(self, "_".join(("in_B", name)))
        self.Q = LogicNode(self, "_".join(("out_Q", name)), enable=False)

    def Evaluate(self):
        self.Q.Set(self.A.value or self.B.value)


class Xor(Edge):

    _type_ = "LogicOperator"

    def __init__(self, name: str):
        super().__init__(name)
        self.A = LogicNode(self, "_".join(("in_A", name)))
        self.B = LogicNode(self, "_".join(("in_B", name)))
        self.Q = LogicNode(self, "_".join(("out_Q", name)), enable=False)

        self.and1 = And("XOR_AND_1")
        self.and2 = And("XOR_AND_2")
        self.not1 = Not("XOR_NOT_1")
        self.not2 = Not("XOR_NOT_2")
        self.or1 = Or("XOR_OR_1")

        self.A.Connect([self.and1.A, self.not2.A])
        self.B.Connect([self.not1.A, self.and2.A])

        self.not1.Q.Connect([self.and1.B])
        self.not2.Q.Connect([self.and2.B])
        self.and1.Q.Connect([self.or1.A])
        self.and2.Q.Connect([self.or1.B])
        self.or1.Q.Connect([self.Q])

    def Evaluate(self):
        pass


def Bit(x, bit):
    return x[bit] == "1"
