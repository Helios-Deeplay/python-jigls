from jils.concrete.base import Base
from jils.logical.logicnode import LogicNode
from jils.logical.logicoperator import Xor, And


class HalfAdder(Base):
    def __init__(self, name: str, dirty: bool = False, enable: bool = True):
        super().__init__(name, dirty, enable)

        self.A = LogicNode(parent=self, name="in_A")
        self.B = LogicNode(parent=self, name="in_B")
        self.S = LogicNode(parent=self, name="out_S")
        self.C = LogicNode(parent=self, name="out_C")

        self.XOR = Xor("XOR")
        self.AND = And("AND")

        self.A.Connect([self.XOR.A, self.AND.A])
        self.B.Connect([self.XOR.B, self.AND.B])
        self.XOR.Q.Connect([self.S])
        self.AND.Q.Connect([self.C])

    def GetNodeValues(self):
        for k, v in self.__dict__.items():
            if isinstance(v, LogicNode):
                print(k, v.value)


def TestHalfAdder():

    instanceHA = HalfAdder("HalfAdder")

    instanceHA.A.Set(False)
    instanceHA.GetNodeValues()

    print("----")

    instanceHA.B.Set(False)
    instanceHA.GetNodeValues()

    print("----")

    instanceHA.B.Set(True)
    instanceHA.GetNodeValues()

    print("----")

    instanceHA.A.Set(True)
    instanceHA.GetNodeValues()


TestHalfAdder()
