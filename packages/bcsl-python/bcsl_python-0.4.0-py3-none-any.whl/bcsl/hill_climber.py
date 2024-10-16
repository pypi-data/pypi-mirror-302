import numpy as np
from causallearn.utils.DAG2CPDAG import dag2cpdag

from bcsl.graph_utils import (
    get_undirected_graph_from_skeleton,
    get_bidirected_edge,
    get_nondirected_edge,
    get_directed_edge,
)


class HillClimber:
    def __init__(self, score_function, get_neighbors_func, node_names):
        """
        Initialize the HillClimber.
        :param score_function: A scoring function (e.g., BDeuScore) to guide the search.
        :param get_neighbors_func: A function from BCSL class to generate neighboring graphs.
        """
        self.score_function = score_function
        self.get_neighbors_func = (
            get_neighbors_func  # Passed function to generate neighbors
        )
        self.node_names = node_names

    def run(self, initial_graph, max_iter=1000):
        """
        Perform hill-climbing search to find the best graph configuration.
        This method will optimize the edge orientations in the graph.
        :param initial_graph: The starting point of the hill-climbing (global skeleton).
        """
        current_graph = initial_graph

        current_score = self.score_function.calculate(current_graph)
        i = 0
        print(f"Hill Climbing started with {max_iter} iterations.")
        print(f"Initial score = {current_score}")
        while i < max_iter:
            if i % 100 == 0:
                print(f"Iteration {i}: Best score = {current_score}")
                print(f"Current graph: {current_graph}")
            neighbors = self.get_neighbors_func(
                current_graph
            )  # Use BCSL's get_neighbors
            best_neighbor = None
            best_score = current_score
            nondirected_edges = set()

            for neighbor in neighbors:
                neighbor_score = self.score_function.calculate(neighbor)
                if neighbor_score > best_score:
                    best_score = neighbor_score
                    best_neighbor = neighbor
                elif np.isclose(neighbor_score, best_score):
                    changed_edges = set(current_graph) - set(neighbor)
                    nondirected_edges.update(changed_edges)

            # If no better neighbor is found, stop
            if best_neighbor is None:
                print(
                    f"Iteration {i}: No better neighbor found. Stopping. Best score = {current_score}"
                )
                break

            current_graph = best_neighbor
            current_score = best_score
            i += 1
            if i == max_iter:
                print(
                    f"Max iteration reached without convergence. Best score = {current_score}"
                )

        graph = get_undirected_graph_from_skeleton(current_graph, self.node_names)
        nodes = graph.nodes
        for edge in nondirected_edges:
            n1 = nodes[edge[0]]
            n2 = nodes[edge[1]]
            edge = graph.get_directed_edge(n1, n2)
            if edge is not None:
                graph.remove_edge(edge)
            edge = graph.get_directed_edge(n2, n1)
            if edge is not None:
                graph.remove_edge(edge)
            graph.add_edge(get_nondirected_edge(n1, n2))

        for edge in current_graph:
            if edge in nondirected_edges:
                continue
            n1 = nodes[edge[0]]
            n2 = nodes[edge[1]]
            edge = graph.get_edge(n1, n2)
            if edge is not None:
                graph.remove_edge(edge)
            edge = graph.get_edge(n2, n1)
            if edge is not None:
                graph.remove_edge(edge)
            graph.add_edge(get_directed_edge(n1, n2))

        return graph
