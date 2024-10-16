import numpy as np

np.mat = np.asmatrix

import numpy as np
from numpy.linalg import LinAlgError


def local_score_BIC(Data: np.ndarray, i: int, PAi: list, parameters=None) -> float:
    """
    Calculate the *negative* local score with BIC for the linear Gaussian continuous data case.
    Adapted from causal-learn with added ridge regression when the covariance matrix is singular.

    Parameters
    ----------
    Data: ndarray, shape (n_samples, n_features)
        The data matrix (samples as rows, features as columns).
    i: int
        The index of the target variable for which the score is calculated.
    PAi: list of int
        The list of parent variable indices.
    parameters: dict, optional
        Dictionary with additional parameters. Expected key is:
        - 'lambda_value': float, penalty discount for BIC (default is 1).

    Returns
    -------
    score: float
        The negative local BIC score for the target variable with the specified parents.
    """

    # Covariance matrix of the data (transpose so features are columns)
    cov = np.cov(Data.T)
    n = Data.shape[0]  # Number of samples

    # Set default lambda_value if not provided
    if parameters is None:
        parameters = {}

    lambda_value = parameters.get("lambda_value", 1) if parameters else 1

    # Case 1: No parents, simply return BIC based on the variance of the target variable
    if len(PAi) == 0:
        return n * np.log(cov[i, i])

    # Case 2: Parents exist, perform regression using the covariance matrix
    # Extract relevant parts of the covariance matrix
    yX = cov[i, PAi]  # Covariance between target i and its parents PAi
    XX = cov[np.ix_(PAi, PAi)]  # Covariance matrix of the parents
    try:
        # Try to invert the XX matrix
        XX_inv = np.linalg.inv(XX)
    except LinAlgError:
        # Add a small perturbation to stabilize the matrix inversion in case of singularity
        epsilon = 1e-5
        XX_inv = np.linalg.inv(XX + epsilon * np.eye(len(PAi)))

    # Compute the conditional variance (variance of i given its parents)
    conditional_variance = cov[i, i] - yX @ XX_inv @ yX.T

    # Ensure conditional variance is positive (if not, we use a small positive value)
    if conditional_variance <= 0:
        conditional_variance = epsilon

    # Compute the log determinant term for the BIC score
    H = np.log(conditional_variance)

    # Return the negative local BIC score
    return n * H + np.log(n) * len(PAi) * lambda_value


class GaussianBICScore:
    def __init__(self, data, parameters=None):
        """
        Initialize the Gaussian BIC score calculator.
        :param data: The dataset used for scoring, where data is a numpy array of shape (n_samples, n_variables).
        :param use_causal_learn: Boolean flag to toggle between custom BIC and causal-learn's BIC.
        """
        self.data = data
        self.n_samples, self.n_vars = data.shape
        self.parameters = parameters

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
        :param var: The target variable index.
        :param parents: A list of parent variable indices for the target variable.
        :return: The BIC score contribution for the variable and its parents.
        """
        score = -local_score_BIC(self.data, var, parents, parameters=self.parameters)
        return score


# Sample usage of GaussianBICScore with causal-learn option
if __name__ == '__main__':
    # Generate synthetic continuous data for testing
    data = np.random.randn(100, 5)  # 100 samples, 5 continuous variables

    # Example graph (DAG) structure as a list of directed edges (parent, child)
    example_graph = [(0, 1), (1, 2), (2, 3), (3, 4)]

    # Initialize Gaussian BIC scoring function with causal-learn option
    gaussian_bic_scorer = GaussianBICScore(data)

    # Calculate BIC score using causal-learn for the example graph
    bic_score = gaussian_bic_scorer.calculate(example_graph)

    print(f"BIC Score: {bic_score}")

