from jigls.concrete.base import Base
from jigls.logical.logicnode import LogicNode
from jigls.logical.logicoperator import Xor, And


class HalfAdder(Base):
    def __init__(
        self, name: str, dirty: bool = False, enable: bool = True
    ):
        super().__init__(name, dirty, enable)

        self.A = LogicNode(parent=self, name="in_A")  # , debug=True)
        self.B = LogicNode(parent=self, name="in_B")  # , debug=True)
        self.S = LogicNode(parent=self, name="out_S")  # , debug=True)
        self.C = LogicNode(parent=self, name="out_C")  # , debug=True)

        self.XOR = Xor("XOR")  # , debug=True)
        self.AND = And("AND")  # , debug=True)

        self.A.AddConnection([self.XOR.A, self.AND.A])
        self.B.AddConnection([self.XOR.B, self.AND.B])
        self.XOR.Q.AddConnection([self.S])
        self.AND.Q.AddConnection([self.C])

    def GetNodeValues(self):
        for k, v in self.__dict__.items():
            if isinstance(v, LogicNode):
                print(k, v.GetValue())


def TestHalfAdder():

    instanceHA = HalfAdder("HalfAdder")

    print("----")

    instanceHA.A.Evaluate(False)
    instanceHA.GetNodeValues()
    # 0 None None 0

    print("----")

    instanceHA.B.Evaluate(False)
    instanceHA.GetNodeValues()
    # 0 0 0 0

    print("----")

    instanceHA.B.Evaluate(True)
    instanceHA.GetNodeValues()
    # 0 1 1 0

    print("----")

    instanceHA.A.Evaluate(True)
    instanceHA.GetNodeValues()
    # 1 1 0 1


# TestHalfAdder()
