from typing import Any, Dict, Iterable, List, Optional, Union


class AbstractOperation(object):
    def __init__(
        self,
        name: str,
        needs: List[str],
        provides: List[str],
        params: Dict = {},
    ):

        self.name = name
        self.needs = needs
        self.provides: List = provides
        self.params = params

        self._after_init()

    def __eq__(self, other):
        return bool(
            self.name is not None
            and self.name == getattr(other, "name", None)
        )

    def __hash__(self):
        return hash(self.name)

    def Compute(self, inputs):
        raise NotImplementedError

    def _Compute(self, named_inputs, outputs=None):
        inputs = [named_inputs[d] for d in self.needs]

        results = self.Compute(inputs)

        results = zip(self.provides, results)

        if outputs:
            outputs = set(outputs)
            results = filter(lambda x: x[0] in outputs, results)

        return dict(results)

    def _after_init(self):
        pass

    def __getstate__(self):
        result = {}
        if hasattr(self, "params"):
            result["params"] = self.__dict__["params"]
        result["needs"] = self.__dict__["needs"]
        result["provides"] = self.__dict__["provides"]
        result["name"] = self.__dict__["name"]

        return result

    def __setstate__(self, state):
        for k in iter(state):
            self.__setattr__(k, state[k])
        self._after_init()

    def __repr__(self):
        return "%s(name='%s', needs=%s, provides=%s)" % (
            self.__class__.__name__,
            self.name,
            self.needs,
            self.provides,
        )


class NetworkOperation(AbstractOperation):
    def __init__(self, **kwargs):
        self.net = kwargs.pop("net")
        super().__init__(**kwargs)

        self._execution_method = "sequential"

    def _Compute(self, named_inputs, outputs=None):
        return self.net.Compute(
            outputs, named_inputs, method=self._execution_method
        )

    def __call__(self, *args, **kwargs):
        return self._Compute(*args, **kwargs)

    def set_execution_method(self, method):
        options = ["parallel", "sequential"]
        assert method in options
        self._execution_method = method

    def plot(self, filename=None, show=False):
        self.net.plot(filename=filename, show=show)

    def __getstate__(self):
        state = AbstractOperation.__getstate__(self)
        state["net"] = self.__dict__["net"]
        return state
