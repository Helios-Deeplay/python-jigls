# from jals.circuit import Base, LNode, Xor, And, Or
from test.halfadder import HalfAdder
from jils.concrete.base import Base
from jils.logical.logicnode import LogicNode
from jils.logical.logicoperator import Or


class FullAdder(Base):  # One bit adder, A,B,Cin in. Sum and Cout out
    def __init__(self, name):
        super().__init__(name)

        self.A = LogicNode(self, "A")
        self.B = LogicNode(self, "B")
        self.Cin = LogicNode(self, "Cin")
        self.S = LogicNode(self, "S")
        self.Cout = LogicNode(self, "Cout")
        self.H1 = HalfAdder("H1")
        self.H2 = HalfAdder("H2")
        self.O1 = Or("O1")

        self.A.AddConnection([self.H1.A])
        self.B.AddConnection([self.H1.B])
        self.Cin.AddConnection([self.H2.A])
        self.H1.S.AddConnection([self.H2.B])
        self.H1.C.AddConnection([self.O1.B])
        self.H2.C.AddConnection([self.O1.A])
        self.H2.S.AddConnection([self.S])
        self.O1.Q.AddConnection([self.Cout])


def testFull(a, b, c):
    F1 = FullAdder("FullAdder")
    F1.Cin.Evaluate(c)
    F1.A.Evaluate(a)
    F1.B.Evaluate(b)

    print("Cin={0}  A={1}  B={2}".format(c, a, b))
    print("Sum={0}  Cout={1}".format(F1.S.value, F1.Cout.value))
