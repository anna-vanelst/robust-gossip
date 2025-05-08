import numpy as np
import networkx as nx


def wn(n, r, alpha=0.1):
    """Compute the weights for the trimmed mean."""
    weights = np.zeros_like(r, dtype=float)
    m = int(alpha * n)
    mask = (m + 0.5 <= r) & (r < n - m + 0.5)
    if n - 2 * m > 0:
        weights[mask] = 1 / (n - 2 * m)
    return weights


def compute_connectivity(graph):
    """Compute lambda_2/|E| for a given graph."""
    m = graph.number_of_edges()
    laplacian = nx.laplacian_matrix(graph).toarray()
    eigenvalues = np.sort(np.linalg.eigvalsh(laplacian))
    lambda_2 = eigenvalues[1]
    return lambda_2 / m
