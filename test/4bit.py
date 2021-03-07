from jals.circuit import Bit
from test.halfadder import HalfAdder
from test.fulladder import FullAdder


def test4Bit(a, b):  # a, b four char strings like '0110'
    F0 = FullAdder("F0")
    F1 = FullAdder("F1")
    F0.Cout.connect(F1.Cin)
    F2 = FullAdder("F2")
    F1.Cout.connect(F2.Cin)
    F3 = FullAdder("F3")
    F2.Cout.connect(F3.Cin)

    F0.Cin.set(0)
    F0.A.set(Bit(a, 3))
    F0.B.set(Bit(b, 3))  # bits in lists are reversed from natural order
    F1.A.set(Bit(a, 2))
    F1.B.set(Bit(b, 2))
    F2.A.set(Bit(a, 1))
    F2.B.set(Bit(b, 1))
    F3.A.set(Bit(a, 0))
    F3.B.set(Bit(b, 0))

    print(
        "{0}{1}{2}{3}{4}".format(
            F3.Cout.value, F3.S.value, F2.S.value, F1.S.value, F0.S.value
        )
    )