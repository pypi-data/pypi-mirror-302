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


def fci_orient_edges_from_graph_node_sepsets(
    data,
    graph,
    nodes,
    sepsets,
    background_knowledge,
    independence_test_method,
    alpha,
    max_path_length,
    verbose,
):
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
