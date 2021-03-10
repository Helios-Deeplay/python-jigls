# from jigls.circuit import Base, StateNode, SetIF


# class SimpleCar(Base):
#     def __init__(self, name):
#         super().__init__(name)

#         self.gear = StateNode(parent=self, name="in_gear", debug=True)
#         self.camera = StateNode(self, "out_camera", debug=True)

#         self.checkGear = SetIF(
#             "Rule001", check="R", setTrue="ON", setFalse="OFF", debug=True
#         )

#         self.gear.connect([self.checkGear.A])
#         # self.checkGear.A.connect(self.gear)
#         self.checkGear.Q.connect(self.camera)

#     def GetNodeValues(self):
#         for k, v in self.__dict__.items():
#             if isinstance(v, StateNode):
#                 print(k, v.value)


# def TestSimpleCar():

#     instanceSC = SimpleCar("SimpleCar")

#     instanceSC.gear.set("D")
#     instanceSC.GetNodeValues()

#     print("----")

#     instanceSC.gear.set("R")
#     instanceSC.GetNodeValues()

#     print("----")

#     instanceSC.gear.set("N")
#     instanceSC.GetNodeValues()


# TestSimpleCar()
