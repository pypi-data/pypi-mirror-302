import time

from causallearn.search.ConstraintBased.FCI import fci

from bcsl.bcsl import BCSL
from bcsl.graph_utils import visualize_graph, get_undirected_graph_from_skeleton


def plot_all_methods(
    data,
    num_bootstrap_samples=1,
    max_k=1,
    conditional_independence_method="kci",
    bootstrap_all_edges=True,
    multiple_comparison_correction=None,
):
    bcsl = BCSL(
        data,
        num_bootstrap_samples=num_bootstrap_samples,
        conditional_independence_method=conditional_independence_method,
        max_k=max_k,
        multiple_comparison_correction=multiple_comparison_correction,
        verbose=False,
    )

    # Step 1: Learn local skeletons using HITON-PC
    start_time = time.time()
    print("Learning Local Skeletons...")
    local_skeletons = bcsl.learn_local_skeleton()
    print("Local Skeletons:", local_skeletons)
    print("Time taken:", time.time() - start_time)

    # Step 2: Resolve asymmetric edges using bootstrap
    start_time = time.time()
    print("Resolving Asymmetric Edges...")
    global_skeleton = bcsl.resolve_asymmetric_edges(
        bootstrap_all_edges=bootstrap_all_edges
    )
    print("Global Skeleton (resolved):", global_skeleton)
    print("Time taken:", time.time() - start_time)
    graph_skeleton = get_undirected_graph_from_skeleton(global_skeleton, data.columns)
    visualize_graph(graph_skeleton, title="BCSL Global Skeleton", show=True)

    # Step 3a: Orient edges using BDeu and hill-climbing
    start_time = time.time()
    print("Orienting Edges using Hill Climbing...")
    dag = bcsl.orient_edges()
    print("Final DAG:", dag)
    visualize_graph(dag, title="Final DAG (Hill Climbing)", show=True)
    print("Time taken:", time.time() - start_time)

    # Step 3b: Orient edges using FCI
    start_time = time.time()
    print("Orienting Edges using BCSL/FCI - KCI...")
    dag_fci = bcsl.orient_edges(method="fci", independence_test_method="kci")
    print("Final DAG (BSCL FCI KCI):", dag_fci)
    visualize_graph(dag_fci, title="Final DAG (BSCL - FCI - KCI)", show=True)
    print("Time taken:", time.time() - start_time)

    # Step 3c: Orient edges using FCI
    start_time = time.time()
    print("Orienting Edges using BCSL/FCI - FisherZ...")
    dag_fci = bcsl.orient_edges(method="fci", independence_test_method="fisherz")
    print("Final DAG (BSCL FCI fisherz):", dag_fci)
    visualize_graph(dag_fci, title="Final DAG (BSCL - FCI - FisherZ)", show=True)
    print("Time taken:", time.time() - start_time)

    # Test vs FCI
    start_time = time.time()
    print("Orienting Edges using FCI - FisherZ from causal-learn...")
    g, edges = fci(data.values, independence_test_method="fisherz")
    print("FCI Graph:", g)
    visualize_graph(
        g, title="FCI Graph Causal Learn FisherZ", show=True, labels=data.columns
    )
    print("Time taken:", time.time() - start_time)

    # Test vs FCI - KCI
    start_time = time.time()
    print("Orienting Edges using FCI - KCI from causal-learn...")
    g, edges = fci(data.values, independence_test_method="kci")
    print("FCI Graph:", g)
    visualize_graph(
        g, title="FCI Graph Causal Learn KCI", show=True, labels=data.columns
    )
    print("Time taken:", time.time() - start_time)
