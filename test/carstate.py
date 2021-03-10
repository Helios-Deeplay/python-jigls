from jigls.concrete.base import Base
from jigls.state.statenode import StateNode
from jigls.state.stateoperator import EvaluateIF


class SimpleCar(Base):
    def __init__(self, name):
        super().__init__(name)

        self.gear = StateNode(parent=self, name="in_gear", debug=True)
        self.camera = StateNode(self, "out_camera", debug=True)

        self.checkGear = EvaluateIF(
            "Rule001", Check="R", IfValue="ON", ElseValue="OFF", debug=True
        )

        self.gear.AddConnection([self.checkGear.A])
        self.checkGear.Q.AddConnection(self.camera)

    def GetNodeValues(self):
        for k, v in self.__dict__.items():
            if isinstance(v, StateNode):
                print(k, v.GetValue())


def TestSimpleCar():

    instanceSC = SimpleCar("SimpleCar")

    instanceSC.gear.Evaluate("D")
    instanceSC.GetNodeValues()

    print("----")

    instanceSC.gear.Evaluate("R")
    instanceSC.GetNodeValues()

    print("----")

    instanceSC.gear.Evaluate("N")
    instanceSC.GetNodeValues()


TestSimpleCar()
