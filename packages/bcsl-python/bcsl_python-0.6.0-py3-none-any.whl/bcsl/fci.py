from typing import Tuple, List, Set, Dict

import numpy as np
from causallearn.graph.Node import Node
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.graph.Edge import Edge
from causallearn.graph.Endpoint import Endpoint
from causallearn.search.ConstraintBased.FCI import (
    reorientAllWith,
    rule0,
    removeByPossibleDsep,
    rulesR1R2cycle,
    ruleR3,
    ruleR4B,
    get_color_edges,
)
from causallearn.utils.PCUtils import BackgroundKnowledge
from causallearn.utils.cit import CIT


def fci_orient_edges_from_graph_node_sepsets(
    data: np.ndarray,
    graph: GeneralGraph,
    nodes: List[Node],
    sepsets: Dict[Tuple[int, int], Set[int]],
    background_knowledge: BackgroundKnowledge,
    independence_test_method: str,
    alpha: float,
    max_path_length: int,
    verbose: bool,
) -> Tuple[GeneralGraph, List[Edge]]:
    """
    Orient edges in a graph using the FCI algorithm from a graph, nodes, sepsets.
    :param data: np.ndarray: The data.
    :param graph: GeneralGraph: The original graph, unoriented.
    :param nodes: List[Node]: The nodes in the graph.
    :param sepsets: Dict[Tuple[int, int], Set[int]]: The sepsets.
    :param background_knowledge: BackgroundKnowledge: The background knowledge.
    :param independence_test_method: str: The independence test method.
    :param alpha: float: The alpha value.
    :param max_path_length: int: The maximum path length.
    :param verbose: bool: Whether to print progress.
    :return:
    """
    independence_test_method = CIT(data, method=independence_test_method)
    reorientAllWith(graph, Endpoint.CIRCLE)
    rule0(graph, nodes, sepsets, knowledge=background_knowledge, verbose=False)
    removeByPossibleDsep(graph, independence_test_method, alpha, sepsets)
    reorientAllWith(graph, Endpoint.CIRCLE)
    rule0(graph, nodes, sepsets, knowledge=background_knowledge, verbose=False)
    change_flag = True
    first_time = True
    while change_flag:
        change_flag = False
        change_flag = rulesR1R2cycle(graph, background_knowledge, change_flag, verbose)
        change_flag = ruleR3(graph, sepsets, background_knowledge, change_flag, verbose)

        if change_flag or (
            first_time
            and background_knowledge is not None
            and len(background_knowledge.forbidden_rules_specs) > 0
            and len(background_knowledge.required_rules_specs) > 0
            and len(background_knowledge.tier_map.keys()) > 0
        ):
            change_flag = ruleR4B(
                graph=graph,
                maxPathLength=max_path_length,
                data=data,
                independence_test_method=independence_test_method,
                alpha=alpha,
                sep_sets=sepsets,
                change_flag=change_flag,
                bk=background_knowledge,
                verbose=verbose,
            )

            first_time = False

            if verbose:
                print("Epoch")
    graph.set_pag(True)
    edges = get_color_edges(graph)
    return graph, edges
