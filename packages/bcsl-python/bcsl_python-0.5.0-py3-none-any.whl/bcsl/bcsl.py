import numpy as np
import pandas as pd
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from causallearn.utils.cit import CIT
from tqdm import tqdm

from bcsl.aee import (
    get_aee_threshold,
    get_observed_aee_threshold,
)
from bcsl.fci import fci_orient_edges_from_graph_node_sepsets
from bcsl.graph_utils import get_undirected_graph_from_skeleton
from bcsl.hill_climber import HillClimber
from bcsl.hiton import Hiton
from bcsl.scores.bdeu import BDeuScore
from bcsl.scores.gaussian_bic import GaussianBICScore


class BCSL:
    def __init__(
        self,
        data,
        num_bootstrap_samples=100,
        max_k=3,
        is_discrete=False,
        orientation_method="hill_climbing",
        conditional_independence_method="fisherz",
        bootstrap_all_edges=True,
        use_aee_alpha=0.05,
        multiple_comparison_correction=None,
        verbose=False,
    ):
        """
        Initialize the BCSL algorithm.
        :param data: The dataset to be used (n x m), where n is samples and m is variables.
        :param num_bootstrap_samples: Number of bootstrap samples for integrated learning.
        :param max_k: Maximum number of variables to condition on in independence tests.
        :param is_discrete: Whether the data is discrete or continuous.
        :param orientation_method: The method to use for edge orientation (hill_climbing or fci).
        :param conditional_independence_method: The method to use for conditional independence tests from causal-learn.
        :param bootstrap_all_edges: Whether to bootstrap all edges after local skeleton learning or only asymmetric edges detected on the whole dataset.
        :param use_aee_alpha: Alpha to use the AEE alpha threshold for resolving asymmetric edges.
        :param multiple_comparison_correction: The method to use for multiple comparison correction. Default is None. Options are: 'bonferroni', 'fdr'.
        :param verbose: Whether to print verbose output.
        """
        if isinstance(data, pd.DataFrame):
            self.node_names = list(data.columns)
            data = data.values
        else:
            self.node_names = [f"X{i}" for i in range(data.shape[1])]
        self.data = data
        self.num_bootstrap_samples = num_bootstrap_samples
        self.conditional_independence_method = conditional_independence_method
        self.local_skeletons = None
        self.global_skeleton = None
        self.sepsets = {}
        self.dag = None
        self.max_k = max_k
        self.is_discrete = is_discrete
        self.orientation_method = orientation_method
        self.bootstrap_all_edges = bootstrap_all_edges
        self.use_aee_alpha = use_aee_alpha
        self.verbose = verbose
        self._cit = None

        self.hiton = Hiton(
            n_vars=self.data.shape[1],
            conditional_independence_test=self.conditional_independence_test,
            max_k=max_k,
            verbose=verbose,
            multiple_comparison_correction=multiple_comparison_correction,
        )

    def conditional_independence_test(self, X, Y, Z=None):
        """
        Perform a conditional independence test to determine if X and Y are independent given Z.
        For discrete data, a chi-squared test is used. For continuous data, partial correlation is used.
        :param X: The target variable (index in dataset).
        :param Y: The variable being tested for dependency with X.
        :param Z: The set of variables to condition on (can be empty).
        :return: p-value from the conditional independence test.
        """
        if self._cit is None:
            if self.is_discrete:
                self._cit = CIT(
                    self.data,
                    method="chisq",
                )
            else:
                self._cit = CIT(
                    self.data,
                    method=self.conditional_independence_method,
                )
        p_value = self._cit(X, Y, Z)
        return p_value

    def learn_local_skeleton(self, directed=False):
        """
        Step 1: Learn the local skeleton (Markov Blanket set) for each variable using HITON.
        """
        n_vars = self.data.shape[1]
        local_skeletons = []
        if self.sepsets is None:
            self.sepsets = {}

        if self.verbose:
            loop_range = tqdm(range(n_vars), desc="Local Skeletons")
        else:
            loop_range = range(n_vars)
        for i in loop_range:
            mb_set, skeleton, sepsets, _ = self.hiton(
                i
            )  # Find the Markov Blanket set for variable i
            local_skeletons.append(skeleton)
            self.merge_sepsets(sepsets)

        if not directed:
            local_skeletons = [
                set(self.make_edges_undirected(edges)) for edges in local_skeletons
            ]

        self.local_skeletons = local_skeletons
        return self.local_skeletons

    def merge_sepsets(self, sepsets):
        """
        Merge the sepsets from each variable into a global sepset dictionary.
        :param sepsets: The sepsets to merge.
        """
        for key, value in sepsets.items():
            if key not in self.sepsets:
                self.sepsets[key] = value
            else:
                self.sepsets[key] = self.sepsets[key].union(value)
        self.ensure_sepset_symmetry()

    def ensure_sepset_symmetry(self):
        """
        Ensure that the sepsets are symmetric (X, Y) -> Z and (Z, Y) -> X are the same.
        """
        for key, value in self.sepsets.items():
            if key[::-1] not in self.sepsets:
                self.sepsets[key[::-1]] = value
            else:
                self.sepsets[key[::-1]] = self.sepsets[key[::-1]].union(value)
                self.sepsets[key] = self.sepsets[key[::-1]]

    def get_bootstrap_subsamples(self):
        """
        Generate bootstrap subsamples from the dataset for integrated learning.
        """
        n_samples = self.data.shape[0]
        subsamples = []
        for _ in range(self.num_bootstrap_samples):
            indices = np.random.choice(n_samples, size=n_samples, replace=True)
            subsample = self.data[indices, :]
            subsamples.append(subsample)
        return subsamples

    def compute_f1_score(self, original_skeleton, learned_skeleton):
        """
        Compute the F1 score between the original skeleton and the learned skeleton for each variable.
        :param original_skeleton: The original skeleton (from the original dataset).
        :param learned_skeleton: The learned skeleton from the subsample.
        :return: F1 score.
        """
        tp = len(
            set(original_skeleton).intersection(learned_skeleton)
        )  # True positives
        fp = len(set(learned_skeleton) - set(original_skeleton))  # False positives
        fn = len(set(original_skeleton) - set(learned_skeleton))  # False negatives

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        if precision + recall == 0:
            return 0  # Avoid division by zero

        f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score

    def resolve_asymmetric_edges(self, directed=False, w=1.1, bootstrap_all_edges=None):
        """
        Step 2: Resolve asymmetric edges using bootstrap subsamples and AEE scoring.

        :param directed: Whether to consider directed edges from local skeletons (default: False).
        :param w: The weight to apply to the F1 score when resolving ties (default: 1.1).
        :param bootstrap_all_edges: Whether to bootstrap all edges (default: False).
        """
        if bootstrap_all_edges is None:
            bootstrap_all_edges = self.bootstrap_all_edges
        original_skeletons = self.local_skeletons
        if original_skeletons is None:
            print(
                "Local skeletons have not been learned yet. Learning local skeletons..."
            )
            original_skeletons = self.learn_local_skeleton(
                directed=directed
            )  # Learn the original skeleton
        subsamples = self.get_bootstrap_subsamples()  # Get bootstrap subsamples

        # Prepare structure to store the weight matrix for each edge
        asymmetric_edges, symmetric_edges = self.find_asymmetric_edges(
            original_skeletons, directed=directed
        )

        if bootstrap_all_edges:
            print("Bootstrapping all edges from the local skeletons...")
            asymmetric_edges = symmetric_edges + asymmetric_edges
            symmetric_edges = []

        if not asymmetric_edges:
            print("No asymmetric edges found. Returning the global skeleton...")
            self.global_skeleton = symmetric_edges
            return self.global_skeleton

        weight_matrices = {
            edge: np.zeros((2, self.num_bootstrap_samples)) for edge in asymmetric_edges
        }
        score_matrices = {
            edge: np.zeros((2, self.num_bootstrap_samples)) for edge in asymmetric_edges
        }

        # For each subsample, learn the skeleton and compute F1 scores
        for j, subsample in tqdm(
            enumerate(subsamples),
            total=len(subsamples),
            desc="Bootstrap Samples",
        ):
            self.data = subsample  # Temporarily replace data with subsample
            learned_skeleton = self.learn_local_skeleton(directed=directed)

            # Calculate F1 score for each variable pair in asymmetric edges
            for edge in asymmetric_edges:
                X_a, X_b = edge
                f1_a = self.compute_f1_score(
                    original_skeletons[X_a], learned_skeleton[X_a]
                )
                f1_b = self.compute_f1_score(
                    original_skeletons[X_b], learned_skeleton[X_b]
                )

                # Store F1 scores in the weight matrix
                weight_matrices[edge][0, j] = f1_a  # F1 score for X_a
                weight_matrices[edge][1, j] = f1_b  # F1 score for X_b

                # Score the edge 1 if in learned skeleton, -1 otherwise
                score_matrices[edge][0, j] = 1 if edge in learned_skeleton[X_a] else -1
                score_matrices[edge][1, j] = 1 if edge in learned_skeleton[X_b] else -1

        threshold = 0
        if self.use_aee_alpha is not None:
            threshold = get_observed_aee_threshold(
                score_matrices, weight_matrices, self.use_aee_alpha
            )
            # w = np.mean(
            #     [np.mean(weight_matrix) for weight_matrix in weight_matrices.values()]
            # )
            # rho = np.mean(
            #     [
            #         np.var(score_matrix.flatten())
            #         for score_matrix in score_matrices.values()
            #     ]
            # )
            # threshold = get_aee_threshold(
            #     self.num_bootstrap_samples, w, rho, self.use_aee_alpha
            # )

        # Now perform AEE scoring for each edge
        resolved_edges = symmetric_edges.copy()
        for edge, weight_matrix in weight_matrices.items():
            score_matrix = score_matrices[edge]
            aee_score = np.sum(score_matrix * weight_matrix)
            if aee_score == 0:
                winner = np.argmax(weight_matrix, axis=0)
                selector = np.where(winner == 0)
                weight_matrix[0, selector] = weight_matrix[0, selector] * w
                selector = np.where(winner == 1)
                weight_matrix[1, selector] = weight_matrix[1, selector] * w
                aee_score = np.sum(score_matrix * weight_matrix)

            if aee_score > threshold:
                resolved_edges.append(
                    edge
                )  # Keep the edge if the AEE score is positive
            else:
                # Remove sepset
                self.sepsets = {
                    key: value
                    for key, value in self.sepsets.items()
                    if key != edge and (not directed or key[::-1] != edge)
                }

        # The final global skeleton after resolving asymmetric edges
        self.global_skeleton = resolved_edges
        return self.global_skeleton

    def find_asymmetric_edges_mb(self, markov_blankets):
        """
        Identify asymmetric edges in the markov_blanket.
        :param markov_blankets: The learned skeleton from the original dataset.
        :return: List of asymmetric edges.
        """
        asymmetric_edges = []
        symmetric_edges = []
        n_vars = len(markov_blankets)
        for i in range(n_vars):
            for j in range(i + 1, n_vars):
                if (i in markov_blankets[j]) and (j not in markov_blankets[i]):
                    asymmetric_edges.append((i, j))
                elif (j in markov_blankets[i]) and (i not in markov_blankets[j]):
                    asymmetric_edges.append((i, j))
                elif (i in markov_blankets[j]) and (j in markov_blankets[i]):
                    symmetric_edge = (i, j) if i < j else (j, i)
                    if symmetric_edge not in asymmetric_edges:
                        symmetric_edges.append(symmetric_edge)
        return asymmetric_edges, symmetric_edges

    def find_asymmetric_edges(self, skeletons, directed=False):
        """
        Identify asymmetric edges in the skeleton.
        :param skeletons: The learned skeleton from the original dataset.
        :param directed: Whether to consider directed edges (default: False).
        :return: List of asymmetric edges.
        """
        asymmetric_edges = []
        symmetric_edges = []
        if not directed:
            # Sort each edge to make them undirected
            skeletons = [set(self.make_edges_undirected(edges)) for edges in skeletons]
        else:
            skeletons = [set(edges) for edges in skeletons]
        n_vars = len(skeletons)
        for i in range(n_vars):
            for j in range(i + 1, n_vars):
                edges_with_j = [edge for edge in skeletons[i] if j in edge]
                for edge in edges_with_j:
                    if edge in skeletons[j]:
                        symmetric_edges.append(edge)
                    else:
                        asymmetric_edges.append(edge)
        asymmetric_edges = list(set(asymmetric_edges))
        symmetric_edges = list(set(symmetric_edges))
        return asymmetric_edges, symmetric_edges

    def make_edges_undirected(self, edges):
        """
        Make the edges undirected by sorting each edge.
        :param edges: The list of edges to make undirected.
        :return: List of undirected edges.
        """
        return list(set([tuple(sorted(edge)) for edge in edges]))

    def orient_edges(self, method=None, independence_test_method="kci"):
        """
        Step 3: Orient the edges in the global skeleton.
        """
        if self.global_skeleton is None:
            print(
                "Global skeleton has not been learned or resolved yet. Learning global skeleton..."
            )
            self.global_skeleton = self.resolve_asymmetric_edges()
        if method is None:
            method = self.orientation_method
        if method == "hill_climbing":
            graph = self.orient_edges_hill_climbing()
            return graph
        elif method == "fci":
            graph, edges = self.orient_edges_fci(
                independence_test_method=independence_test_method
            )
            return graph
        else:
            raise ValueError(f"Unknown orientation method: {method}")

    def orient_edges_hill_climbing(self):
        """
        Orient the edges in the global skeleton using BDeu or Gaussian BIC and hill-climbing.
        :return:  The final directed acyclic graph (DAG).
        """
        if self.global_skeleton is None:
            raise ValueError("Global skeleton has not been learned or resolved yet.")

        # Initialize the BDeu score function
        if self.is_discrete:
            score_function = BDeuScore(self.data, ess=1.0, use_causal_learn=True)
        else:
            score_function = GaussianBICScore(self.data)

        # Initialize hill-climbing with the global skeleton and BDeu scoring
        hill_climber = HillClimber(
            score_function, self.get_neighbors, node_names=self.node_names
        )
        self.dag = hill_climber.run(
            self.global_skeleton
        )  # Run hill-climbing to orient edges

        return self.dag

    def orient_edges_fci(
        self,
        max_path_length: int = -1,
        depth: int = -1,
        independence_test_method="kci",
        alpha=0.05,
        verbose=False,
        background_knowledge=None,
        **kwargs,
    ):
        """
        Orient the edges in the global skeleton using FCI algorithm from causal-learn.
        Perform Fast Causal Inference (FCI) algorithm for causal discovery

        Parameters
        ----------
        dataset: data set (numpy ndarray), shape (n_samples, n_features). The input data, where n_samples is the number of
                samples and n_features is the number of features.
        independence_test_method: str, name of the function of the independence test being used
                [fisherz, chisq, gsq, kci]
               - fisherz: Fisher's Z conditional independence test
               - chisq: Chi-squared conditional independence test
               - gsq: G-squared conditional independence test
               - kci: Kernel-based conditional independence test
        alpha: float, desired significance level of independence tests (p_value) in (0,1)
        depth: The depth for the fast adjacency search, or -1 if unlimited
        max_path_length: the maximum length of any discriminating path, or -1 if unlimited.
        verbose: True is verbose output should be printed or logged
        background_knowledge: background knowledge

        Returns
        -------
        graph : a GeneralGraph object, where graph.graph[j,i]=1 and graph.graph[i,j]=-1 indicates  i --> j ,
                        graph.graph[i,j] = graph.graph[j,i] = -1 indicates i --- j,
                        graph.graph[i,j] = graph.graph[j,i] = 1 indicates i <-> j,
                        graph.graph[j,i]=1 and graph.graph[i,j]=2 indicates  i o-> j.
        edges : list
            Contains graph's edges properties.
            If edge.properties have the Property 'nl', then there is no latent confounder. Otherwise,
                there are possibly latent confounders.
            If edge.properties have the Property 'dd', then it is definitely direct. Otherwise,
                it is possibly direct.
            If edge.properties have the Property 'pl', then there are possibly latent confounders. Otherwise,
                there is no latent confounder.
            If edge.properties have the Property 'pd', then it is possibly direct. Otherwise,
                it is definitely direct.
        """

        # if dataset.shape[0] < dataset.shape[1]:
        #     warnings.warn("The number of features is much larger than the sample size!")
        #
        independence_test_method = CIT(
            self.data, method=independence_test_method, **kwargs
        )

        if (depth is None) or type(depth) != int:
            raise TypeError("'depth' must be 'int' type!")
        if (background_knowledge is not None) and type(
            background_knowledge
        ) != BackgroundKnowledge:
            raise TypeError(
                "'background_knowledge' must be 'BackgroundKnowledge' type!"
            )
        if type(max_path_length) != int:
            raise TypeError("'max_path_length' must be 'int' type!")

        graph = get_undirected_graph_from_skeleton(
            skeleton=self.global_skeleton, node_names=self.node_names
        )
        nodes = graph.nodes

        graph, edges = fci_orient_edges_from_graph_node_sepsets(
            data=self.data,
            graph=graph,
            nodes=nodes,
            sepsets=self.sepsets,
            background_knowledge=background_knowledge,
            independence_test_method=independence_test_method,
            alpha=alpha,
            max_path_length=max_path_length,
            verbose=verbose,
        )

        return graph, edges

    def get_neighbors(self, graph):
        """
        Generate neighbor graphs by changing the orientation of one edge at a time.
        :param graph: The current graph structure.
        :return: A list of neighboring graphs.
        """
        graph = set(graph)  # Convert to set for faster edge lookup
        neighbors = []
        for edge in graph:
            neighbor = graph.copy()
            # Flip edge orientation (X -> Y becomes Y -> X)
            X, Y = edge
            neighbor.remove(edge)
            neighbor.add((Y, X))  # Flip the edge
            neighbors.append(list(neighbor))
        return neighbors
