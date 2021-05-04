import logging
import time
from itertools import chain
from typing import Dict

import networkx as nx
from jengine.logger import logger

from .base import AbstractOperation
from .data import Data, DataPlaceholderNode, DeleteInstruction, ParamArgs

logger = logging.getLogger(__name__)


class Network(object):
    def __init__(self, **kwargs):

        self.graph: nx.DiGraph = nx.DiGraph()
        self._debug = kwargs.get("debug", False)

        self.times = {}
        self.steps = []
        self._necessary_steps_cache = {}

    def AddOperation(self, operation: AbstractOperation):

        assert operation.name, "Operation must be named"

        assert operation.needs is not None, "Operation's 'needs' must be named"

        assert operation.provides is not None, "Operation's 'provides' must be named"

        assert operation not in self.graph.nodes(), "Operation may only be added once"

        for n in operation.needs:
            self.graph.add_edge(DataPlaceholderNode(n), operation)

        for p in operation.provides:
            self.graph.add_edge(operation, DataPlaceholderNode(p))

        for k, v in operation.params.items():
            self.graph.add_edge(ParamArgs("{%s=%s}" % (k, v)), operation)

        self.steps = []

    def AddEdge(self, source, destination):
        self.graph.add_edge(
            DataPlaceholderNode(source), DataPlaceholderNode(destination)
        )

    def ListLayers(self):

        if not self.steps:
            logger.warning(
                "possible no operations in network / network was not compiled properly"
            )

        return [(s.name, s) for s in self.steps if isinstance(s, AbstractOperation)]

    def ShowLayers(self):
        for name, step in self.ListLayers():
            print("layer_name: ", name)
            print("\t", "needs: ", step.needs)
            print("\t", "provides: ", step.provides)
            print("")

    def Compile(self):
        self.steps.clear()

        executionOrder = list(nx.topological_sort(self.graph))

        for i, node in enumerate(executionOrder):

            # print(node)

            if isinstance(node, DataPlaceholderNode):
                continue

            if isinstance(node, ParamArgs):
                continue

            elif isinstance(node, AbstractOperation):
                self.steps.append(node)

                for predecessor in self.graph.predecessors(node):
                    if self._debug:
                        print("checking if node %s can be deleted" % predecessor)

                    predecessor_still_needed = False

                    for future_node in executionOrder[i + 1 :]:
                        if isinstance(future_node, AbstractOperation):
                            if predecessor in future_node.needs:
                                predecessor_still_needed = True
                                break

                    if not predecessor_still_needed:
                        if self._debug:
                            print("  adding delete instruction for %s" % predecessor)
                        self.steps.append(DeleteInstruction(predecessor))

            else:
                raise TypeError("Unrecognized network graph node %s" % node)

    def _EvaluateNecessarySteps(self, outputs, inputs):
        outputs = (
            tuple(sorted(outputs)) if isinstance(outputs, (list, set)) else outputs
        )

        inputs_keys = tuple(sorted(inputs.keys()))
        cache_key = (inputs_keys, outputs)

        if cache_key in self._necessary_steps_cache:
            return self._necessary_steps_cache[cache_key]

        graph = self.graph

        if not outputs:
            necessary_nodes = set()
            for input_name in iter(inputs):
                if graph.has_node(input_name):
                    necessary_nodes |= nx.descendants(graph, input_name)

        else:
            unnecessary_nodes = set()
            for input_name in iter(inputs):
                if graph.has_node(input_name):
                    unnecessary_nodes |= nx.ancestors(graph, input_name)

            necessary_nodes = set()
            for output_name in outputs:
                if not graph.has_node(output_name):
                    raise ValueError(
                        "network graph does not have an output "
                        "node named %s" % output_name
                    )
                necessary_nodes |= nx.ancestors(graph, output_name)

            necessary_nodes -= unnecessary_nodes

        necessary_steps = [step for step in self.steps if step in necessary_nodes]

        # save this result in a precomputed cache for future lookup
        self._necessary_steps_cache[cache_key] = necessary_steps

        # Return an ordered list of the needed steps.
        return necessary_steps

    def Compute(self, outputs, named_inputs, method=None):

        # assert that network has been compiled
        assert self.steps, "network must be compiled before calling compute."

        assert (
            isinstance(outputs, (list, tuple)) or outputs is None
        ), "The outputs argument must be a list"

        if method == "parallel":
            return self._ThreadPool(named_inputs, outputs)
        else:
            return self._Sequential(named_inputs, outputs)

    def isReadyToScheduleOperation(self, op, has_executed, graph):
        dependencies = set(
            filter(
                lambda v: isinstance(v, AbstractOperation),
                nx.ancestors(graph, op),
            )
        )
        return dependencies.issubset(has_executed)

    def isReadyToDeleteDataNode(self, name, has_executed, graph):
        data_node = GetDataNode(name, graph)
        return set(graph.successors(data_node)).issubset(has_executed)

    # ! need to be worked on !!
    # ? currently only support single threaded execution
    def _ThreadPool(self, named_inputs, outputs, thread_pool_size=10):
        """
        This method runs the graph using a parallel pool of thread executors.
        """
        raise NotImplementedError(
            "not implemented, revert to single threaded execution"
        )
        # from multiprocessing.dummy import Pool

        # if not hasattr(self, "_thread_pool"):
        #     self._thread_pool = Pool(thread_pool_size)

        # pool = self._thread_pool

        # cache = {}
        # cache.update(named_inputs)
        # necessary_nodes = self._EvaluateNecessarySteps(
        #     outputs, named_inputs
        # )

        # has_executed = set()

        # while True:
        #     upnext = []

        #     for node in necessary_nodes:
        #         if isinstance(node, DeleteInstruction):
        #             if self.isReadyToDeleteDataNode(
        #                 node, has_executed, self.graph
        #             ):
        #                 if node in cache:
        #                     cache.pop(node)

        #         if not isinstance(node, AbstractOperation):
        #             continue

        #         if (
        #             self.isReadyToScheduleOperation(
        #                 node, has_executed, self.graph
        #             )
        #             and node not in has_executed
        #         ):
        #             upnext.append(node)

        #     if len(upnext) == 0:
        #         break

        #     done_iterator = pool.imap_unordered(
        #         lambda op: (op, op._Compute(cache)), upnext
        #     )

        #     for op, result in done_iterator:
        #         cache.update(result)
        #         has_executed.add(op)

        # if not outputs:
        #     return cache
        # else:
        #     return {k: cache[k] for k in iter(cache) if k in outputs}

    def _Sequential(self, named_inputs, outputs):
        """
        This method runs the graph one operation at a time in a single thread
        """
        cache = {}

        cache.update(named_inputs)

        all_steps = self._EvaluateNecessarySteps(outputs, named_inputs)

        self.times = {}
        for step in all_steps:

            if isinstance(step, AbstractOperation):

                if self._debug:
                    print("-" * 32)
                    print("executing step: %s" % step.name)

                t0 = time.time()

                layer_outputs = step.Compute(cache)

                self._CacheUpdateOutput(cache, layer_outputs)
                # cache.update(layer_outputs)

                t_complete = round(time.time() - t0, 5)
                self.times[step.name] = t_complete

                if self._debug:
                    print("step completion time: %s" % t_complete)

            elif isinstance(step, DeleteInstruction):
                if outputs and step not in outputs:
                    if step in cache:
                        if self._debug:
                            print("removing data '%s' from cache." % step)
                        cache.pop(step)

            else:
                raise TypeError("Unrecognized instruction.")

        if not outputs:
            return cache

        else:
            return {k: cache[k] for k in iter(cache) if k in outputs}

    # ! should be provided and overwritten by data class
    def _CacheUpdateOutput(self, cache: Dict[str, Data], output: Dict[str, Data]):
        for k, v in output.items():
            if k in cache:
                if v.GetData():
                    cache[k].SetData(v.GetData())
                cache[k].SetEnable(v.GetEnable())
            else:
                cache[k] = v

    def Plot(
        self,
        filepath: str = r"results/",
        filename: str = "temp",
        show: bool = False,
        cleanup: bool = True,
    ):

        from graphviz import Digraph as DiDotViz

        assert self.graph is not None

        def GetNodeName(a):
            if isinstance(a, (DataPlaceholderNode, ParamArgs)):
                return a
            return a.name

        g = DiDotViz(comment="network")
        g.attr(splines="ortho")
        g.attr(overlap="false")

        for node in self.graph.nodes:
            if isinstance(node, DataPlaceholderNode):
                g.node(name=node, shape="rect")
            elif isinstance(node, ParamArgs):
                g.node(name=node, shape="octagon")
            else:
                g.node(name=node.name, shape="circle")

        # draw edges
        for src, dst in self.graph.edges:
            g.edge(GetNodeName(src), GetNodeName(dst))

        # save plot
        path = "".join((filepath, filename))

        if show:
            input(
                g.render(path, view=show, format="pdf", cleanup=cleanup),
            )
            input(
                g.render(path, view=show, format="png", cleanup=cleanup),
            )
        else:
            g.render(path, view=show, format="pdf", cleanup=cleanup)
            g.render(path, view=show, format="png", cleanup=cleanup)


class NetworkOperation(AbstractOperation):
    def __init__(self, net: Network, **kwargs):
        self.net = net
        super().__init__(**kwargs)
        self._executionMethod = "sequential"

    def _Compute(self, named_inputs, outputs=None):
        return self.net.Compute(outputs, named_inputs, method=self._executionMethod)

    def __call__(self, *args, **kwargs):
        return self._Compute(*args, **kwargs)

    def SetExecutionMethod(self, method):
        options = ["parallel", "sequential"]
        assert method in options
        self._executionMethod = method

    def Plot(self, filename="temp", show=False, cleanup=True):
        self.net.Plot(filename=filename, show=show, cleanup=cleanup)

    def __getstate__(self):
        state = AbstractOperation.__getstate__(self)
        state["net"] = self.__dict__["net"]
        return state


class NetworkCompose(object):
    def __init__(self, name=None, merge=False):
        assert name, "compose needs a name"
        self.name = name
        self.merge = merge

    def __call__(self, *operations: AbstractOperation):

        assert len(operations), "no operations provided to compose"

        if self.merge:
            merge_set = set()
            for op in operations:
                if isinstance(op, NetworkOperation):
                    net_ops = filter(
                        lambda x: isinstance(x, AbstractOperation),
                        op.net.steps,
                    )
                    merge_set.update(net_ops)
                else:
                    merge_set.add(op)
            operations = tuple(merge_set)

        def OrderPreservingUniquifier(seq, seen=None):
            seen = seen if seen else set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        provides = OrderPreservingUniquifier(chain(*[op.provides for op in operations]))
        needs = OrderPreservingUniquifier(
            chain(*[op.needs for op in operations]), set(provides)
        )

        # compile network
        net = Network()
        for op in operations:
            net.AddOperation(op)
        net.Compile()

        return NetworkOperation(
            net=net,
            name=self.name,
            needs=needs,
            provides=provides,
            params={},
        )


def GetDataNode(name, graph):
    for node in graph.nodes:
        if node == name and isinstance(node, DataPlaceholderNode):
            return node
    return None
