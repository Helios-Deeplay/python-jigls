import math
import unittest
from operator import add, mul, sub
from typing import Dict, Tuple

from jigls import JiglsCompose, JiglsOperation


class TestCore(unittest.TestCase):
    def test_sum(self):
        """bind operation function"""

        op_sum = JiglsOperation(
            name="op_sum", needs=["a", "b"], provides="sum_ab"
        )(add)

        self.assertEqual(op_sum(1, 2), 3)

    def test_decorator(self):
        """decorator compute function"""

        @JiglsOperation(
            name="op_mul", needs=["sum_ab", "b"], provides="sum_ab_times_b"
        )
        def op_mul(a, b):
            return a * b

        self.assertEqual(op_mul(2, 2), 4)

    def test_lateBind(self):
        """partial bind operation function"""

        op_partial = JiglsOperation(
            name="op_partial",
            needs=["sum_ab_p1", "sum_ab_p2"],
            provides="p1_plus_p2",
        )

        op = op_partial(add)
        self.assertEqual(op(5, 6), 11)

    def test_earlyBind(self):
        """early binding function"""

        op = JiglsOperation(add)

        op_sum = op(name="sum_op3", needs=["a", "b"], provides="sum_ab2")

        self.assertEqual(op_sum(6, 6), 12)

    def test_param(self):
        """param test compute function"""

        @JiglsOperation(
            name="op_pow",
            needs="ab",
            provides=["ab_p0", "ab_p1", "ab_p2", "ab_p3"],
            params={"exponent": 3},
        )
        def op_pow(a, exponent=2):
            return [math.pow(a, y) for y in range(0, exponent + 1)]

        result = op_pow._Compute({"ab": 2})

        self.assertIn("ab_p0", result)
        self.assertIn("ab_p1", result)
        self.assertIn("ab_p2", result)
        self.assertIn("ab_p3", result)

        self.assertEqual(result["ab_p0"], 1)
        self.assertEqual(result["ab_p1"], 2)
        self.assertEqual(result["ab_p2"], 4)
        self.assertEqual(result["ab_p3"], 8)

    def test_compose(self):

        op_sum = JiglsOperation(
            name="op_sum", needs=["a", "b"], provides="sum_ab"
        )(add)

        @JiglsOperation(
            name="op_mul",
            needs=["sum_ab", "b"],
            provides="sum_ab_times_b",
        )
        def op_mul(a, b):
            return a * b

        @JiglsOperation(
            name="op_pow",
            needs="sum_ab",
            provides=["sum_ab_p1", "sum_ab_p2", "sum_ab_p3"],
            params={"exponent": 3},
        )
        def op_pow(a, exponent=2):
            return [math.pow(a, y) for y in range(1, exponent + 1)]

        op_partial = JiglsOperation(
            name="op_sum_partial",
            needs=["sum_ab_p1", "sum_ab_p2"],
            provides="p1_plus_p2",
        )
        op_sum_partial = op_partial(add)

        op_factory = JiglsOperation(add)
        op_sum_factory = op_factory(
            name="op_sum_early", needs=["a", "b"], provides="sum_ab2"
        )

        net = JiglsCompose(name="my network")(
            op_sum, op_mul, op_pow, op_sum_partial, op_sum_factory
        )

        result = net({"a": 1, "b": 2})
        check = {
            "a": 1,
            "b": 2,
            "p1_plus_p2": 12.0,
            "sum_ab": 3,
            "sum_ab2": 3,
            "sum_ab_p1": 3.0,
            "sum_ab_p2": 9.0,
            "sum_ab_p3": 27.0,
            "sum_ab_times_b": 6,
        }
        self.assertEqual(result, check)

    def test_plot(self):
        """test plot pdf and png"""

        def abspow(a, p):
            return abs(a) ** p

        # Compose the mul, sub, and abspow operations into a computation graph.
        net = JiglsCompose(name="graph")(
            JiglsOperation(name="mul1", needs=["a", "b"], provides=["ab"])(
                mul
            ),
            JiglsOperation(
                name="sub1", needs=["a", "ab"], provides=["a_minus_ab"]
            )(sub),
            JiglsOperation(
                name="abspow1",
                needs=["a_minus_ab"],
                provides=["abs_a_minus_ab_cubed"],
                params={"p": 3},
            )(abspow),
        )

        net.Plot()
