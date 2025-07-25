import numpy as np
import networkx as nx
import random


def generate_graph(n, type="Watts-Strogatz", seed=42):
    if type == "Complete":
        G = nx.complete_graph(n)
    elif type == "Watts-Strogatz":
        k = 4  # Average degree for Watts-Strogatz
        p = 0.4  # Rewiring probability
        G = nx.watts_strogatz_graph(n, k, p, seed=seed)
    elif type == "2D Grid":
        length, width = best_side_from_surface(n)
        G = nx.grid_2d_graph(length, width)
        G = nx.convert_node_labels_to_integers(G)
    elif type == "Cycle":
        G = nx.cycle_graph(n)
    elif type == "Clustered":
        G = clustered_graph(n)
    else:
        raise ValueError("Wrong graph type.")

    # check if graph is connected
    if not nx.is_connected(G):
        print("Graph is not connected. Generating a new graph.")
        return generate_graph(n, type, seed + 1)
    else:
        return G


def best_side_from_surface(S):
    root = int(S**0.5)
    for i in range(root, 0, -1):
        if S % i == 0:
            j = S // i
            return (i, j)


def clustered_graph(n, clusters=3, intra_prob=0.3, inter_edges=5, seed=42):
    """
    Generate a graph with `n` nodes divided into `clusters` clusters.
    Each cluster has dense intra-cluster edges, and there are a few inter-cluster edges.

    Parameters:
        n (int): Total number of nodes.
        clusters (int): Number of clusters.
        intra_prob (float): Probability of an edge between nodes in the same cluster.
        inter_edges (int): Number of edges connecting different clusters.
        seed (int): Random seed for reproducibility.

    Returns:
        networkx.Graph: The generated clustered graph.
    """
    random.seed(seed)
    nodes_per_cluster = n // clusters
    G = nx.Graph()
    cluster_nodes = []

    # Create clusters
    for i in range(clusters):
        start = i * nodes_per_cluster
        end = (
            start + nodes_per_cluster if i < clusters - 1 else n
        )  # last cluster may take the remainder
        nodes = list(range(start, end))
        cluster_nodes.append(nodes)

        # Intra-cluster connections
        for u in nodes:
            for v in nodes:
                if u < v and random.random() < intra_prob:
                    G.add_edge(u, v)

    # Inter-cluster edges
    for _ in range(inter_edges):
        c1, c2 = random.sample(range(clusters), 2)
        u = random.choice(cluster_nodes[c1])
        v = random.choice(cluster_nodes[c2])
        G.add_edge(u, v)

    return G
