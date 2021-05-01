from typing import Any, Dict, Iterable, List, Optional, Union


class AbstractOperation(object):
    def __init__(
        self,
        name: str = str(),
        needs: List[str] = list(),
        provides: List[str] = list(),
        params: Dict = {},
    ):

        self.name = name
        self.needs = needs
        self.provides = provides
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
