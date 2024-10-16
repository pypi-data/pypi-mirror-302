import numpy as np
import pandas as pd
from causallearn.graph.Edge import Edge
from causallearn.graph.Endpoint import Endpoint
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.graph.GraphNode import GraphNode

from bcsl.graph_utils import visualize_graph
from examples.utilities import plot_all_methods


def compare_easy_dataset(
    num_bootstrap_samples=1, conditional_independence_method="kci"
):
    # Generate synthetic data for testing
    np.random.seed(42)

    # Define True Causal Graph
    true_graph = create_true_causal_graph_easy()
    visualize_graph(true_graph, title="True Causal Graph (EASY)", show=True)

    n_samples = 500

    # Independent variables
    Var0 = np.random.normal(0, 1, n_samples)
    Var1 = np.random.normal(0, 1, n_samples) + Var0 * 3
    Var2 = np.random.normal(0, 1, n_samples) + Var0

    # Dependent variables
    Var3 = 2 * Var1 + np.random.normal(0, 1, n_samples)  # Var3 depends on Var1
    Var4 = 0.5 * Var2 + np.random.normal(0, 1, n_samples)  # Var4 depends on Var2
    Var5 = (
        Var3 + Var4 + np.random.normal(0, 1, n_samples)
    )  # Var5 depends on Var3 and Var4
    data = pd.DataFrame(
        {
            "Var0": Var0,
            "Var1": Var1,
            "Var2": Var2,
            "Var3": Var3,
            "Var4": Var4,
            "Var5": Var5,
        }
    )

    plot_all_methods(
        data,
        num_bootstrap_samples,
        conditional_independence_method=conditional_independence_method,
    )


def create_true_causal_graph_easy() -> GeneralGraph:
    """
    Creates the true causal graph for the easy dataset using causal-learn's GeneralGraph.

    Returns:
    - GeneralGraph: The true causal graph.
    """
    # Define node names
    node_names = ["Var0", "Var1", "Var2", "Var3", "Var4", "Var5"]

    # Create GraphNode instances
    nodes = {name: GraphNode(name) for name in node_names}

    # Initialize GeneralGraph
    graph = GeneralGraph(list(nodes.values()))

    # Define true directed edges
    true_edges = [
        ("Var0", "Var1"),
        ("Var0", "Var2"),
        ("Var1", "Var3"),
        ("Var2", "Var4"),
        ("Var3", "Var5"),
        ("Var4", "Var5"),
    ]

    # Add directed edges to the graph
    for source, target in true_edges:
        edge = Edge(
            nodes[source],
            nodes[target],
            Endpoint.TAIL,  # Tail end for the source node
            Endpoint.ARROW,  # Arrow end for the target node
        )
        graph.add_edge(edge)

    return graph
