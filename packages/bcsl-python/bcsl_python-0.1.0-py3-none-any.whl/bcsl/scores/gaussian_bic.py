from symbol import parameters

import numpy as np
np.mat = np.asmatrix
from causallearn.score.LocalScoreFunction import local_score_BIC

class GaussianBICScore:
    def __init__(self, data, use_causal_learn=False):
        """
        Initialize the Gaussian BIC score calculator.
        :param data: The dataset used for scoring, where data is a numpy array of shape (n_samples, n_variables).
        :param use_causal_learn: Boolean flag to toggle between custom BIC and causal-learn's BIC.
        """
        self.data = data
        self.n_samples, self.n_vars = data.shape
        self.use_causal_learn = use_causal_learn

    def calculate(self, graph):
        """
        Calculate the Gaussian BIC score for a given graph (DAG).
        :param graph: The directed acyclic graph (DAG) structure.
        :return: The Gaussian BIC score for the graph.
        """
        score = 0
        for i in range(self.n_vars):
            parents = self.get_parents(graph, i)  # Get the parents of variable X_i
            score += self.compute_bic_for_variable(i, parents)
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

    def compute_bic_for_variable(self, var, parents):
        """
        Compute the BIC score for a single variable and its parent set.
        If use_causal_learn is set to True, the BIC score will be calculated using causal-learn's local_score_BIC.
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The BIC score contribution for the variable and its parents.
        """
        if self.use_causal_learn:
            # Use causal-learn's BIC scoring function
            score = self.causal_learn_bic(var, parents)
        else:
            # Use the custom Gaussian BIC method
            score = self.custom_gaussian_bic(var, parents)
        return score

    def causal_learn_bic(self, var, parents, parameters=None):
        """
        Use causal-learn's local_score_BIC to compute the BIC score for a variable and its parents.
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The BIC score from causal-learn.
        """
        # Set up the parameters for local_score_BIC (default options can be used)
        score = -local_score_BIC(self.data, var, parents, parameters=parameters)
        return score

    def custom_gaussian_bic(self, var, parents):
        """
        Compute the custom Gaussian BIC score for a single variable and its parent set.
        This implementation uses a multivariate Gaussian model.
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The log-likelihood and complexity penalty for the variable and its parents.
        """
        if len(parents) == 0:
            # No parents: treat as a simple univariate Gaussian
            variance = np.var(self.data[:, var], ddof=1)
            log_likelihood = -0.5 * self.n_samples * np.log(2 * np.pi * variance)
            complexity = 1  # Only the variance parameter
        else:
            # Multiple linear regression for the target variable on its parents
            X = self.data[:, parents]  # Parent variables (design matrix)
            y = self.data[:, var]  # Target variable
            beta_hat = np.linalg.lstsq(X, y, rcond=None)[0]  # OLS regression coefficients
            residuals = y - X @ beta_hat
            variance = np.var(residuals, ddof=1)

            log_likelihood = -0.5 * self.n_samples * np.log(2 * np.pi * variance)
            complexity = len(parents) + 1  # One parameter for each parent plus the variance

        return - log_likelihood + 0.5 * complexity * np.log(self.n_samples)


# Sample usage of GaussianBICScore with causal-learn option
if __name__ == '__main__':
    # Generate synthetic continuous data for testing
    data = np.random.randn(100, 5)  # 100 samples, 5 continuous variables

    # Example graph (DAG) structure as a list of directed edges (parent, child)
    example_graph = [(0, 1), (1, 2), (2, 3), (3, 4)]

    # Initialize Gaussian BIC scoring function with causal-learn option
    gaussian_bic_scorer = GaussianBICScore(data, use_causal_learn=True)

    # Calculate BIC score using causal-learn for the example graph
    bic_score = gaussian_bic_scorer.calculate(example_graph)

    print(f"BIC Score using causal-learn: {bic_score}")

    # Calculate BIC score using custom Gaussian BIC for comparison
    gaussian_bic_scorer_custom = GaussianBICScore(data, use_causal_learn=False)
    bic_score_custom = gaussian_bic_scorer_custom.calculate(example_graph)

    print(f"Custom Gaussian BIC Score: {bic_score_custom}")
