# from jals.circuit import Base, LNode, Xor, And, Or
# from test.halfadder import HalfAdder


# class FullAdder(Base):  # One bit adder, A,B,Cin in. Sum and Cout out
#     def __init__(self, name):
#         super().__init__(name)
#         self.A = LNode(self, "A", 1, debug=1)
#         self.B = LNode(self, "B", 1, debug=1)
#         self.Cin = LNode(self, "Cin", 1, debug=1)
#         self.S = LNode(self, "S", debug=1)
#         self.Cout = LNode(self, "Cout", debug=1)
#         self.H1 = HalfAdder("H1")
#         self.H2 = HalfAdder("H2")
#         self.O1 = Or("O1")
#         self.A.connect([self.H1.A])
#         self.B.connect([self.H1.B])
#         self.Cin.connect([self.H2.A])
#         self.H1.S.connect([self.H2.B])
#         self.H1.C.connect([self.O1.B])
#         self.H2.C.connect([self.O1.A])
#         self.H2.S.connect([self.S])
#         self.O1.C.connect([self.Cout])


# def testFull(a, b, c):
#     F1 = FullAdder("F1")
#     F1.Cin.set(c)
#     F1.A.set(a)
#     F1.B.set(b)

#     print("Cin={0}  A={1}  B={2}".format(c, a, b))
#     print("Sum={0}  Cout={1}".format(F1.S.value, F1.Cout.value))