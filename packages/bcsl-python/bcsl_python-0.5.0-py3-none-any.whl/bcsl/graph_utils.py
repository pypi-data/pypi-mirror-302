import io
from typing import List

import networkx as nx
from causallearn.graph.Edge import Edge
from causallearn.graph.Endpoint import Endpoint
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.graph.GraphNode import GraphNode
from causallearn.graph.Node import Node
from causallearn.utils.GraphUtils import GraphUtils
from matplotlib import pyplot as plt, image as mpimg


def get_all_edges_from(target_var, to_set):
    """
    Get all edges from the target variable to the variables in the given set.
    :param target_var: The target variable index.
    :param to_set: set for  the direct neighbors of the target variable.
    :return: List of edges from the target variable to the variables in to_set.
    """
    edges = []
    for var in to_set:
        if var != target_var:
            edges.append((target_var, var))
    return edges


def get_undirected_graph_from_skeleton(skeleton, node_names):
    """
    Get a graph from the skeleton, considered undirected.
    :param skeleton:  List[Tuple[int, int]]: The skeleton of the graph.
    :param node_names: List[str]: The names of the nodes.
    :return:  GeneralGraph: The graph.
    """
    nodes: List[Node] = []
    for name in node_names:
        node = GraphNode(name)
        nodes.append(node)
    graph: GeneralGraph = GeneralGraph(nodes)
    for edge in skeleton:
        X, Y = edge
        graph.add_edge(Edge(nodes[X], nodes[Y], Endpoint.CIRCLE, Endpoint.CIRCLE))

    return graph


def visualize_graph(graph, labels=None, title=None, output_path=None, show=True):
    """
    Visualizes a causal learn graph.

    Parameters:
    - result: The result object from the causal discovery algorithm.
    - labels (list): Optional list of labels for the nodes.
    - filename (str): Optional filename to save the graph as an image.
    """
    title = title or "Causal Graph"

    if not show and output_path is None:
        raise ValueError("Please specify an output path or set show=True.")
    pyd = GraphUtils.to_pydot(graph, labels=labels, dpi=300)
    tmp_png = pyd.create_png()
    sio = io.BytesIO()
    sio.write(tmp_png)
    sio.seek(0)
    img = mpimg.imread(sio)
    plt.figure(figsize=(16, 16), dpi=300)
    plt.imshow(img)
    plt.axis("off")
    plt.title(title)
    if output_path:
        plt.savefig(output_path, bbox_inches="tight", dpi=300)
        print(f"{title} saved as {output_path}.")
    if show:
        plt.show()


def get_undirected_edge(node1, node2):
    """
    Get an undirected edge between two nodes.
    :param node1: The first node.
    :param node2: The second node.
    :return: Edge: The undirected edge.
    """
    return Edge(node1, node2, Endpoint.TAIL, Endpoint.TAIL)


def get_bidirected_edge(node1, node2):
    """
    Get a bidirected edge between two nodes.
    :param node1: The first node.
    :param node2: The second node.
    :return: Edge: The bidirected edge.
    """
    return Edge(node1, node2, Endpoint.ARROW, Endpoint.ARROW)


def get_nondirected_edge(node1, node2):
    """
    Get a non-directed edge between two nodes.
    :param node1: The first node.
    :param node2: The second node.
    :return: Edge: The non-directed edge.
    """
    return Edge(node1, node2, Endpoint.CIRCLE, Endpoint.CIRCLE)


def get_directed_edge(node1, node2):
    """
    Get a directed edge between two nodes.
    :param node1: The first node.
    :param node2: The second node.
    :return: Edge: The directed edge.
    """
    return Edge(node1, node2, Endpoint.TAIL, Endpoint.ARROW)
