import operator
from typing import Optional, Union

from jigls.concrete.edge import Edge
from jigls.state.statenode import StateNode


class EvaluateIF(Edge):

    _type_ = "StateOperator"

    def __init__(
        self,
        name: str,
        Check: Optional[Union[str, int, float, bool]],
        IfValue: Optional[Union[str, int, float, bool]],
        ElseValue: Optional[Union[str, int, float, bool]],
        debug: bool = False,
    ):
        super().__init__(
            name,
        )

        self.check = Check
        self.ifv = IfValue
        self.elv = ElseValue
        self.A = StateNode(self, "_".join(("in_A", name)), debug=debug)
        self.Q = StateNode(self, "_".join(("out_Q", name)), debug=debug)

    def Evaluate(self):
        if operator.eq(self.A.value, self.check):
            self.Q.Evaluate(self.ifv)
        else:
            self.Q.Evaluate(self.elv)
