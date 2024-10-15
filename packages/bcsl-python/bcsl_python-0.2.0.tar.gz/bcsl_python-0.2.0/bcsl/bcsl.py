from itertools import combinations

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, pearsonr
from tqdm import tqdm

from bcsl.hill_climber import HillClimber
from bcsl.scores.bdeu import BDeuScore
from bcsl.scores.gaussian_bic import GaussianBICScore


class BCSL:
    def __init__(self, data, num_bootstrap_samples=100, max_k=3, is_discrete=False, use_causal_learn=True):
        """
        Initialize the BCSL algorithm.
        :param data: The dataset to be used (n x m), where n is samples and m is variables.
        :param num_bootstrap_samples: Number of bootstrap samples for integrated learning.
        :param max_k: Maximum number of variables to condition on in independence tests.
        :param is_discrete: Whether the data is discrete or continuous.
        :param use_causal_learn: Whether to use causal-learn for conditional independence tests and scoring.
        """
        if isinstance(data, pd.DataFrame):
            data = data.values
        self.data = data
        self.num_bootstrap_samples = num_bootstrap_samples
        self.use_causal_learn = use_causal_learn
        self.local_skeletons = None
        self.global_skeleton = None
        self.dag = None
        self.max_k = max_k
        self.is_discrete = is_discrete

    def conditional_independence_test(self, X, Y, Z=[]):
        """
        Perform a conditional independence test to determine if X and Y are independent given Z.
        For discrete data, a chi-squared test is used. For continuous data, partial correlation is used.
        :param X: The target variable (index in dataset).
        :param Y: The variable being tested for dependency with X.
        :param Z: The set of variables to condition on (can be empty).
        :return: p-value from the conditional independence test.
        """
        if self.is_discrete:
            if len(Z) > 0:
                raise ValueError("Conditional independence test for discrete data does not support conditioning.")
            # Use chi-squared test for discrete data
            observed = np.histogram2d(self.data[:, X], self.data[:, Y], bins=2)[0]
            chi2, p_value, _, _ = chi2_contingency(observed)
            return p_value
        else:
            # Use partial correlation for continuous data
            if len(Z) == 0:
                # Pearson correlation if no conditioning
                _, p_value = pearsonr(self.data[:, X], self.data[:, Y])
                return p_value
            elif self.use_causal_learn:
                from causallearn.utils.cit import CIT
                kci_obj = CIT(self.data, "kci")
                p_value = kci_obj(X, Y, Z)
                return p_value
            else:
                # Perform partial correlation test (using the external method for simplicity)
                raise ValueError("Partial correlation test not implemented for continuous data.")

    def hiton(self, target_var, alpha=0.05, spouses=True):
        """
        HITON algorithm to find the Markov Blanket (MB) set for a target variable.
        This combines HITON-PC for the Parents and Children and the Spouse discovery.
        :param target_var: The target variable index.
        :param alpha: Significance level for the conditional independence test.
        :param spouses: Whether to discover spouses (default: True).
        :return: The MB set (indices of variables in the Markov Blanket), skeleton, sepset, and ci_count.
        """
        n_vars = self.data.shape[1]
        candidate_set = list(range(n_vars))
        candidate_set.remove(target_var)  # Remove the target itself
        ci_count = 0  # Counter for the number of conditional independence tests
        sepset = [[] for _ in range(n_vars)]  # Separating sets

        # Step 1: HITON-PC (Parents and Children discovery)
        variDepSet = []
        for var in candidate_set:
            p_value = self.conditional_independence_test(target_var, var)
            ci_count += 1
            if p_value < alpha:  # Dependent variables
                variDepSet.append([var, p_value])

        # Sort candidate variables by dependency (smaller p-value means stronger dependency)
        variDepSet = sorted(variDepSet, key=lambda x: x[1])
        candidate_PC = [var[0] for var in variDepSet]  # Candidate PC set

        # Shrink phase: Test conditional independence with subsets of other variables in the PC set
        pc_set = candidate_PC[:]
        for x in candidate_PC:
            conditions_Set = [i for i in pc_set if i != x]

            # Limit the size of conditional sets based on max_k
            for k in range(min(self.max_k, len(conditions_Set)) + 1):
                if x not in pc_set:
                    break
                for subset in combinations(conditions_Set, k):
                    p_value = self.conditional_independence_test(target_var, x, list(subset))
                    ci_count += 1
                    if p_value >= alpha:  # If conditionally independent
                        sepset[x] = list(subset)  # Store the separating set
                        pc_set.remove(x)
                        break

        currentMB = pc_set.copy()
        current_skeleton = self.get_all_edges_from(target_var, currentMB)
        direct_neighbors = currentMB.copy()

        # Step 2: Spouse Discovery
        if spouses:
            for x in pc_set:
                PCofPC, _, _, ci_num2 = self.hiton(x, alpha,
                                                spouses=False)  # Find PC of each PC variable (Spouse discovery)
                ci_count += ci_num2

                for y in PCofPC:
                    if y != target_var and y not in direct_neighbors:
                        # Add conditioning on x (spouse candidate) for the target variable
                        conditions_Set = sepset[y] + [x]
                        conditions_Set = list(set(conditions_Set))  # Avoid duplicates
                        pval = self.conditional_independence_test(target_var, y, conditions_Set)
                        ci_count += 1
                        if pval <= alpha:
                            currentMB.append(y)  # Add spouse to the Markov Blanket
                            # X is a collider Target -> X <- Y
                            current_skeleton.append((y, x))  # Add edge from x to y
                            # Orient the edge from Target to X
                            # current_skeleton.remove((target_var, y))
                            # current_skeleton.remove((y, target_var))
                            # current_skeleton.add((target_var, y, "o")) or something

        return list(set(currentMB)), set(current_skeleton), sepset, ci_count

    def get_all_edges_from(self, target_var, to_set):
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

    def learn_local_skeleton(self, directed=False):
        """
        Step 1: Learn the local skeleton (Markov Blanket set) for each variable using HITON.
        """
        n_vars = self.data.shape[1]
        local_skeletons = []

        for i in range(n_vars):
            mb_set, skeleton, sepset, _ = self.hiton(i)  # Find the Markov Blanket set for variable i
            local_skeletons.append(skeleton)

        if not directed:
            local_skeletons = [set(self.make_edges_undirected(edges)) for edges in local_skeletons]

        self.local_skeletons = local_skeletons
        return self.local_skeletons

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
        tp = len(set(original_skeleton).intersection(learned_skeleton))  # True positives
        fp = len(set(learned_skeleton) - set(original_skeleton))  # False positives
        fn = len(set(original_skeleton) - set(learned_skeleton))  # False negatives

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        if precision + recall == 0:
            return 0  # Avoid division by zero

        f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score

    def resolve_asymmetric_edges(self, directed=False, w=1.1):
        """
        Step 2: Resolve asymmetric edges using bootstrap subsamples and AEE scoring.
        """
        original_skeletons = self.learn_local_skeleton(directed=directed)  # Learn the original skeleton
        subsamples = self.get_bootstrap_subsamples()  # Get bootstrap subsamples

        # Prepare structure to store the weight matrix for each edge
        asymmetric_edges, symmetric_edges = self.find_asymmetric_edges(original_skeletons, directed=directed)
        weight_matrices = {edge: np.zeros((2, self.num_bootstrap_samples)) for edge in asymmetric_edges}
        score_matrices = {edge: np.zeros((2, self.num_bootstrap_samples)) for edge in asymmetric_edges}

        # For each subsample, learn the skeleton and compute F1 scores
        for j, subsample in tqdm(enumerate(subsamples), total=self.num_bootstrap_samples, desc="Bootstrap Samples"):
            self.data = subsample  # Temporarily replace data with subsample
            learned_skeleton = self.learn_local_skeleton(directed=directed)

            # Calculate F1 score for each variable pair in asymmetric edges
            for edge in asymmetric_edges:
                X_a, X_b = edge
                f1_a = self.compute_f1_score(original_skeletons[X_a], learned_skeleton[X_a])
                f1_b = self.compute_f1_score(original_skeletons[X_b], learned_skeleton[X_b])

                # Store F1 scores in the weight matrix
                weight_matrices[edge][0, j] = f1_a  # F1 score for X_a
                weight_matrices[edge][1, j] = f1_b  # F1 score for X_b

                # Score the edge 1 if in learned skeleton, -1 otherwise
                score_matrices[edge][0, j] = 1 if edge in learned_skeleton[X_a] else -1
                score_matrices[edge][1, j] = 1 if edge in learned_skeleton[X_b] else -1

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

            if aee_score > 0:
                resolved_edges.append(edge)  # Keep the edge if the AEE score is positive

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


    def orient_edges(self):
        """
        Step 3: Orient the edges in the global skeleton using BDeu and hill-climbing.
        """
        if self.global_skeleton is None:
            raise ValueError("Global skeleton has not been learned or resolved yet.")

        # Initialize the BDeu score function
        if self.is_discrete:
            score_function = BDeuScore(self.data, ess=1.0, use_causal_learn=self.use_causal_learn)
        else:
            score_function = GaussianBICScore(self.data, use_causal_learn=self.use_causal_learn)

        # Initialize hill-climbing with the global skeleton and BDeu scoring
        hill_climber = HillClimber(score_function, self.get_neighbors)
        self.dag = hill_climber.run(self.global_skeleton)  # Run hill-climbing to orient edges

        return self.dag

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
