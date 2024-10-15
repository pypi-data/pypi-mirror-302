from fmot import fqir
from collections import defaultdict
import numpy as np
from .helpers import replace_tensor_in_graph
from ordered_set import OrderedSet as set


def uniquify_names(graph: fqir.GraphProto):
    try:
        arith = graph.subgraphs["ARITH"]
    except:
        arith = graph

    name2tensors = defaultdict(set)

    def add_tensor(x: fqir.TensorProto):
        name2tensors[x.name].add(x)

    for node in arith.nodes:
        for x in node.inputs.values():
            add_tensor(x)
        for x in node.outputs:
            add_tensor(x)

    for name, tensors in name2tensors.items():
        if len(tensors) > 1:
            for i, t in enumerate(tensors):
                t.name = f"{name}.{i}"

    return graph


def correct_subgraph_outputs(graph: fqir.GraphProto):
    """Ensures that subgraph outputs tensorprotos match the outputs from the
    graphs themselves."""
    for node in graph.nodes:
        if node.subgraph is not None:
            outputs = node.subgraph.outputs
            node.outputs = outputs

            correct_subgraph_outputs(node.subgraph)


def limit_biases(graph: fqir.GraphProto):
    """Restrict biases to the symmetric range [-2**(B-1)+1, 2**(B-1)-1]"""
    for node in graph.subgraphs["ARITH"].nodes:
        if node.opname == "addmm":
            bias = node.inputs["bias"]
            if bias.dtype == "fqint8":
                bw = 8
            else:
                bw = 16

            val = bias.value
            if val is not None:
                val = np.clip(val, -(2 ** (bw)) + 1, 2 ** (bw) - 1)
                bias.value = val


def remove_unused_params(graph: fqir.GraphProto):
    """Strips graph of unused parameters"""
    arith = graph.subgraphs["ARITH"]
    unused_params = set(arith.parameters)

    for node in arith.nodes:
        for inp in node.inputs.values():
            if inp in unused_params:
                unused_params.remove(inp)

    for param in unused_params:
        arith.parameters.remove(param)


def remove_null_shifts(graph: fqir.GraphProto):
    """Strips graph of shift-by-zero"""
    arith = graph.subgraphs["ARITH"]

    def remove_one_null_shift(graph: fqir.GraphProto):
        for node in graph.nodes:
            if node.opname == "shift":
                x = node.inputs["x"]
                y = node.outputs[0]
                shamt = node.constants["shamt"]

                if x.dtype == y.dtype and shamt == 0:
                    replace_tensor_in_graph(y, x, graph)
                    graph.nodes.remove(node)
                    return True
        return False

    while remove_one_null_shift(arith):
        pass
