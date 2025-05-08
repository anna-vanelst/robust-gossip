import numpy as np
import networkx as nx


def generate_graph(n, type="Watts-Strogatz", seed=42):
    if type == "Complete":
        G = nx.complete_graph(n)
    elif type == "Watts-Strogatz":
        k = 4  # Average degree for Watts-Strogatz
        p = 0.4  # Rewiring probability
        G = nx.watts_strogatz_graph(n, k, p, seed=seed)
    elif type == "Watts-Strogatz-d6":
        k = 6  # Average degree for Watts-Strogatz
        p = 0.8  # Rewiring probability
        G = nx.watts_strogatz_graph(n, k, p, seed=seed)
    elif type == "2D Grid":
        length, width = best_side_from_surface(n)
        G = nx.grid_2d_graph(length, width)
        G = nx.convert_node_labels_to_integers(G)
    elif type == "Cycle":
        G = nx.cycle_graph(n)
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
