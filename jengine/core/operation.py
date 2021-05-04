import operator
from typing import Callable, Dict, List
from .base import AbstractOperation
from .data import OptionalArg


class Operation(AbstractOperation):
    def __init__(
        self,
        name: str,
        needs: List[str],
        provides: List[str],
        params: Dict = {},
        fn: Callable = None,
    ):
        self.fn = fn
        super().__init__(name, needs, provides, params)

    def Compute(self, named_inputs, outputs=None):

        inputs = [named_inputs[d] for d in self.needs if not isinstance(d, OptionalArg)]

        optionals = {
            n: named_inputs[n]
            for n in self.needs
            if isinstance(n, OptionalArg) and n in named_inputs
        }

        kwargs = {k: v for d in (self.params, optionals) for k, v in d.items()}

        result = self.fn(*inputs, **kwargs)  # type:ignore

        if len(self.provides) == 1:
            result = [result]

        result = zip(self.provides, result)

        if outputs:
            outputs = set(outputs)
            result = filter(lambda x: x[0] in outputs, result)

        return dict(result)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __getstate__(self):
        state = super().__getstate__()
        state["fn"] = self.__dict__["fn"]
        return state

    def __repr__(self):
        func_name = getattr(self, "fn")
        func_name = func_name and getattr(func_name, "__name__", None)
        return u"%s(name='%s', needs=%s, provides=%s, fn=%s)" % (
            self.__class__.__name__,
            self.name,
            self.needs,
            self.provides,
            func_name,
        )


class OperationCompose(AbstractOperation):
    def __init__(
        self,
        name: str = str(),
        needs: List[str] = list(),
        provides: List[str] = list(),
        params: Dict = {},
        fn: Callable = None,
    ):

        self.fn = fn
        super().__init__(name, needs, provides, params)

    @staticmethod
    def CheckKwargs(kwargs):

        assert kwargs["name"], "operation needs a name"

        if "needs" in kwargs and type(kwargs["needs"]) == str:
            assert kwargs["needs"], "empty string provided for `needs` parameters"

            kwargs["needs"] = [kwargs["needs"]]

        # Allow single value for provides parameter
        if "provides" in kwargs and type(kwargs["provides"]) == str:
            assert kwargs["provides"], "empty string provided for `needs` parameters"

            kwargs["provides"] = [kwargs["provides"]]

        assert type(kwargs["needs"]) == list, "no `needs` parameter provided"

        assert type(kwargs["provides"]) == list, "no `provides` parameter provided"

        assert hasattr(
            kwargs["fn"], "__call__"
        ), "operation was not provided with a callable"

        if type(kwargs["params"]) is not dict:
            kwargs["params"] = {}

        return kwargs

    def __call__(self, fn: Callable = None, **kwargs):

        if fn is not None:
            self.fn = fn

        _kwargs = {}
        _kwargs.update(vars(self))
        _kwargs.update(kwargs)
        _kwargs = OperationCompose.CheckKwargs(_kwargs)

        return Operation(**_kwargs)

    def __repr__(self):
        func_name = getattr(self, "fn") and getattr(
            getattr(self, "fn"), "__name__", None
        )
        return u"%s(name='%s', needs=%s, provides=%s, fn=%s)" % (
            self.__class__.__name__,
            self.name,
            self.needs,
            self.provides,
            func_name,
        )
