import numpy as np
from scipy.stats import norm


def compute_aee_variance(N, w, rho):
    """
    Compute the variance of AEE_score = sum(V_i), where V_i = Score_i * weight_i
    Assuming:
    - All weight_i = w
    - Covariance between any two Scores = rho

    Parameters:
    - N (int): Total number of bootstrap samples
    - w (float): Weight for each V_i, in [0,1]
    - rho (float): Covariance between any two Scores

    Returns:
    - float: Variance of S
    """
    return N * w**2 * (1 + (N - 1) * rho)


def get_aee_threshold(N, w, rho, alpha):
    """
    Get the AEE threshold for a given alpha, N, w, and rho.

    Parameters:
    - alpha (float): Significance level
    - N (int): Total number of bootstrap samples
    - w (float): Weight for each V_i, in [0,1]
    - rho (float): Covariance between any two Scores

    Returns:
    - float: AEE threshold
    """
    variance = compute_aee_variance(N, w, rho)
    std_dev = np.sqrt(variance)
    alpha_quantile = np.abs(norm.ppf(alpha))
    return alpha_quantile * std_dev


def compute_observed_aee_variance(score_matrices, weight_matrices):
    """
    Compute the variance of AEE_score = sum(V_i), where V_i = Score_i * weight_i
    for the observed data.

    Parameters:
    - score_matrices (List[np.ndarray]): List of score matrices
    - weight_matrices (List[np.ndarray]): List of weight matrices

    Returns:
    - float: Variance of S
    """
    scores = []
    for edge in score_matrices.keys():
        score_matrix = score_matrices[edge]
        weight_matrix = weight_matrices[edge]
        scores.append(np.sum(score_matrix * weight_matrix))
    return np.var(scores)


def get_observed_aee_threshold(score_matrices, weight_matrices, alpha):
    """
    Get the AEE threshold for the observed data.

    Parameters:
    - score_matrices (List[np.ndarray]): List of score matrices
    - weight_matrices (List[np.ndarray]): List of weight matrices
    - alpha (float): Significance level (unilateral)

    Returns:
    - float: AEE threshold
    """
    variance = compute_observed_aee_variance(score_matrices, weight_matrices)
    std_dev = np.sqrt(variance)
    alpha_quantile = np.abs(norm.ppf(alpha))
    return alpha_quantile * std_dev
