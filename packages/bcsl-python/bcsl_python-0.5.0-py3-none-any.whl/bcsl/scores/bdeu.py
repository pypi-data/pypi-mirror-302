import numpy as np
np.mat = np.asmatrix
from causallearn.score.LocalScoreFunction import local_score_BDeu
from scipy.special import gammaln  # Logarithm of the Gamma function


class BDeuScore:
    def __init__(self, data, ess=1.0, use_causal_learn=False):
        """
        Initialize the BDeu score calculator.
        :param data: The dataset used for scoring, where data is a numpy array of shape (n_samples, n_variables).
        :param ess: Equivalent sample size (ESS), a hyperparameter for prior counts.
        """
        self.data = data
        self.n_samples, self.n_vars = data.shape
        self.ess = ess
        self.use_causal_learn = use_causal_learn

    def calculate(self, graph):
        """
        Calculate the BDeu score for a given graph (DAG).
        :param graph: The directed acyclic graph (DAG) structure.
        :return: The BDeu score for the graph.
        """
        score = 0
        for i in range(self.n_vars):
            parents = self.get_parents(graph, i)  # Get the parents of variable X_i
            score += self.compute_bdeu_for_variable(i, parents)
        return score

    def get_parents(self, graph, var):
        """
        Get the parent variables for a given variable based on the graph structure.
        :param graph: The DAG structure (a list of edges).
        :param var: The variable for which to get the parents.
        :return: A list of parent variables for var.
        """
        parents = []
        for edge in graph:
            if edge[1] == var:
                parents.append(edge[0])
        return parents

    def compute_bdeu_for_variable(self, var, parents):
        """
        Compute the BDeu score for a single variable and its parent set.
        If use_causal_learn is set to True, the BDeu score will be calculated using causal-learn's local_score_BDeu.
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The BDeu score contribution for the variable and its parents.
        """
        if self.use_causal_learn:
            # Use causal-learn's BDeu scoring function
            score = self.causal_learn_bdeu(var, parents)
        else:
            # Use the custom BDeu method
            score = self.custom_bdeu(var, parents)
        return score

    def causal_learn_bdeu(self, var, parents, parameters=None):
        """
        Use causal-learn's local_score_BDeu to compute the BDeu score for a variable and its parents.
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The BDeu score from causal-learn.
        """
        bdeu_score = -local_score_BDeu(self.data, var, parents, parameters=parameters)
        return bdeu_score

    def custom_bdeu(self, var, parents):
        """
        Compute the BDeu score for a single variable and its parent set.
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The BDeu score contribution for the variable and its parents.
        """
        # Get the unique values for the variable and its parents
        unique_var_values = np.unique(self.data[:, var])
        parent_configs, parent_counts = self.get_parent_configurations(parents)

        # Number of parent configurations and number of possible values for the variable
        num_parent_configs = parent_configs.shape[0]
        num_var_values = len(unique_var_values)

        # Alpha (prior) values for each variable and parent combination
        alpha_i = self.ess / (num_var_values * num_parent_configs)

        score = 0

        # Loop over each parent configuration
        for parent_config_idx in range(num_parent_configs):
            # Find the subset of samples where the parents match the current configuration
            parent_mask = np.all(self.data[:, parents] == parent_configs[parent_config_idx], axis=1)
            parent_count = parent_counts[parent_config_idx]

            # Compute the terms for BDeu
            score += gammaln(alpha_i) - gammaln(alpha_i + parent_count)

            for var_value in unique_var_values:
                # Count the number of instances where the variable has a specific value, given the parent configuration
                var_value_count = np.sum(self.data[parent_mask, var] == var_value)

                score += gammaln(alpha_i + var_value_count) - gammaln(alpha_i)

        return score

    def get_parent_configurations(self, parents):
        """
        Get the possible configurations of parent values and the counts for each configuration.
        :param parents: A list of parent variable indices.
        :return: A tuple (parent_configs, parent_counts), where parent_configs is a list of unique
                 parent value combinations, and parent_counts is the count of each combination in the dataset.
        """
        if len(parents) == 0:
            return np.array([[]]), np.array([self.n_samples])

        # Get the unique combinations of parent values
        parent_values = self.data[:, parents]
        parent_configs, parent_counts = np.unique(parent_values, axis=0, return_counts=True)

        return parent_configs, parent_counts


# Sample usage of BDeuScore
if __name__ == '__main__':
    # Generate synthetic data for testing
    data = np.random.randint(0, 2, size=(100, 5))  # 100 samples, 5 binary variables (0 or 1)

    # Example graph (DAG) structure as a list of directed edges (parent, child)
    example_graph = [(0, 1), (1, 2), (2, 3), (3, 4)]

    # Initialize BDeu scoring function
    bdeu_scorer = BDeuScore(data, ess=1.0)

    # Calculate BDeu score for the example graph
    bdeu_score = bdeu_scorer.calculate(example_graph)

    print(f"BDeu Score Custom: {bdeu_score}")

    # Calculate BDeu score using causal-learn for comparison
    bdeu_scorer_causal_learn = BDeuScore(data, ess=1.0, use_causal_learn=True)
    bdeu_score_causal_learn = bdeu_scorer_causal_learn.calculate(example_graph)

    print(f"BDeu Score using causal-learn: {bdeu_score_causal_learn}")



