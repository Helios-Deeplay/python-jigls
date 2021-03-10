from jigls.logical.logicoperator import Bit
from test.fulladder import FullAdder


def test4Bit(a, b):  # a, b four char strings like '0110'
    F0 = FullAdder("F0")
    F1 = FullAdder("F1")
    F0.Cout.AddConnection(F1.Cin)
    F2 = FullAdder("F2")
    F1.Cout.AddConnection(F2.Cin)
    F3 = FullAdder("F3")
    F2.Cout.AddConnection(F3.Cin)

    F0.Cin.Evaluate(False)
    F0.A.Evaluate(Bit(a, 3))
    F0.B.Evaluate(
        Bit(b, 3)
    )  # bits in lists are reversed from natural order
    F1.A.Evaluate(Bit(a, 2))
    F1.B.Evaluate(Bit(b, 2))
    F2.A.Evaluate(Bit(a, 1))
    F2.B.Evaluate(Bit(b, 1))
    F3.A.Evaluate(Bit(a, 0))
    F3.B.Evaluate(Bit(b, 0))

    print(
        "{0} {1} {2} {3} {4}".format(
            F3.Cout.GetValue(),
            F3.S.GetValue(),
            F2.S.GetValue(),
            F1.S.GetValue(),
            F0.S.GetValue(),
        )
    )  # 0 0 1 1 0


test4Bit("0100", "0010")