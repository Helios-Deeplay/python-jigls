from jals.circuit import Base, LNode, Xor, And


class HalfAdder(Base):
    def __init__(self, name):
        super().__init__(name)

        self.A = LNode(parent=self, name="in_A", debug=True)
        self.B = LNode(parent=self, name="in_B", debug=True)
        self.S = LNode(self, "out_S", debug=True)
        self.C = LNode(self, "out_C", debug=True)

        self.XOR = Xor("XOR", debug=True)
        self.AND = And("AND", debug=True)

        self.A.connect([self.XOR.A, self.AND.A])
        self.B.connect([self.XOR.B, self.AND.B])
        self.XOR.Q.connect([self.S])
        self.AND.Q.connect([self.C])

    def GetNodeValues(self):
        for k, v in self.__dict__.items():
            if isinstance(v, LNode):
                print(k, v.value)


def TestHalfAdder():

    instanceHA = HalfAdder("HalfAdder")

    instanceHA.A.set(0)
    instanceHA.GetNodeValues()

    print("----")

    instanceHA.B.set(0)
    instanceHA.GetNodeValues()

    print("----")

    instanceHA.B.set(1)
    instanceHA.GetNodeValues()

    print("----")

    instanceHA.A.set(1)
    instanceHA.GetNodeValues()


TestHalfAdder()
