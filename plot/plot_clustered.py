import networkx as nx
import random
import matplotlib.pyplot as plt
from src.graph import clustered_graph


# Generate and plot the graph using the function
G = clustered_graph(n=100, clusters=3)
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 8))
nx.draw(
    G, pos, with_labels=False, node_size=50, node_color="skyblue", edge_color="gray"
)
plt.title("Generated Clustered Graph")
plt.show()
