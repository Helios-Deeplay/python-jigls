from .base import AbstractOperation
from .data import OptionalArg


class FunctionalOperation(AbstractOperation):
    def __init__(self, **kwargs):
        self.fn = kwargs.pop("fn")
        super().__init__(**kwargs)

    def _Compute(self, named_inputs, outputs=None):

        inputs = [
            named_inputs[d]
            for d in self.needs
            if not isinstance(d, OptionalArg)
        ]

        optionals = {
            n: named_inputs[n]
            for n in self.needs
            if isinstance(n, OptionalArg) and n in named_inputs
        }

        kwargs = {
            k: v for d in (self.params, optionals) for k, v in d.items()
        }

        result = self.fn(*inputs, **kwargs)

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


class JiglsOperation(AbstractOperation):
    def __init__(self, fn=None, **kwargs):

        self.fn = fn
        super().__init__(**kwargs)

    def _CheckKwargs(self, kwargs):

        assert kwargs["name"], "operation needs a name"

        if "needs" in kwargs and type(kwargs["needs"]) == str:
            assert kwargs[
                "needs"
            ], "empty string provided for `needs` parameters"

            kwargs["needs"] = [kwargs["needs"]]

        # Allow single value for provides parameter
        if "provides" in kwargs and type(kwargs["provides"]) == str:
            assert kwargs[
                "provides"
            ], "empty string provided for `needs` parameters"

            kwargs["provides"] = [kwargs["provides"]]

        assert (
            type(kwargs["needs"]) == list
        ), "no `needs` parameter provided"

        assert (
            type(kwargs["provides"]) == list
        ), "no `provides` parameter provided"

        assert hasattr(
            kwargs["fn"], "__call__"
        ), "operation was not provided with a callable"

        if type(kwargs["params"]) is not dict:
            kwargs["params"] = {}

        return kwargs

    def __call__(self, fn=None, **kwargs):

        if fn is not None:
            self.fn = fn

        _kwargs = {}
        _kwargs.update(vars(self))
        _kwargs.update(kwargs)
        _kwargs = self._CheckKwargs(_kwargs)

        return FunctionalOperation(**_kwargs)

    def __repr__(self):
        return u"%s(name='%s', needs=%s, provides=%s)" % (
            self.__class__.__name__,
            self.name,
            self.needs,
            self.provides,
        )
