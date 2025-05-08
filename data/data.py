import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import networkx as nx
import pickle
import matplotlib.pyplot as plt


def geo_distance(loc1, loc2):
    """
    Calculate the distance between two points on the earth
    using the Haversine formula.
    """
    loc1 = [radians(_) for _ in loc1]
    loc2 = [radians(_) for _ in loc2]
    res = haversine_distances([loc1, loc2])
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return r * res[0, 1]


threshold = 1
df = pd.read_csv(
    "data/100009@basel-stadt.csv", sep=";", encoding="utf-8", header=0, low_memory=False
)
df = df.dropna(subset=["Koordinaten"])
df = df.dropna(subset=["Lufttemperatur"])
agg_df = df.groupby("Name").first().reset_index()
agg_df[["latitude", "longitude"]] = agg_df["Koordinaten"].str.split(",", expand=True)
agg_df["latitude"] = agg_df["latitude"].astype(float)
agg_df["longitude"] = agg_df["longitude"].astype(float)
agg_df = agg_df.reset_index(drop=True)
agg_df["id"] = agg_df.index

# construct a graph from the agg_df dataframe using geo_distance saying
# two point are connected if the distance is less than 1 km
G = nx.Graph()
for i, row in agg_df.iterrows():
    G.add_node(row["id"], pos=(row["latitude"], row["longitude"]))
for i, row in agg_df.iterrows():
    for j, row2 in agg_df.iterrows():
        if (
            i != j
            and geo_distance(
                loc1=[row["latitude"], row["longitude"]],
                loc2=[row2["latitude"], row2["longitude"]],
            )
            < 1.0
        ):
            G.add_edge(row["id"], row2["id"])
for i, row in agg_df.iterrows():
    G.nodes[row["id"]]["temperature"] = row["Lufttemperatur"]
    G.nodes[row["id"]]["latitude"] = row["latitude"]
    G.nodes[row["id"]]["longitude"] = row["longitude"]
# keep the largest connected component of the graph
largest_cc = max(nx.connected_components(G), key=len)
G_sub = G.subgraph(largest_cc).copy()
degree = dict(G_sub.degree)
print("Average degree of the graph", np.mean(list(degree.values())))
print("Min degree", np.min(list(degree.values())))
print("Number of nodes", len(G_sub.nodes()))

# removes nodes with degree <= threshold and corresponding edges
nodes_to_remove = [node for node, degree in G_sub.degree() if degree <= threshold]
G_sub.remove_nodes_from(nodes_to_remove)
G_sub = nx.convert_node_labels_to_integers(G_sub)
degree = dict(G_sub.degree)
print("Number of nodes", len(G_sub.nodes()))
print("Average degree of the graph", np.mean(list(degree.values())))
print("Min degree", np.min(list(degree.values())))
plt.figure(figsize=(6, 4))
nx.draw(
    G_sub,
    pos=nx.get_node_attributes(G_sub, "pos"),
    with_labels=False,
    node_size=50,
    font_size=15,
    node_color=[G_sub.nodes[i]["temperature"] for i in G_sub.nodes()],
    cmap="viridis",
)
plt.axis("off")
plt.savefig(f"data/graph_{threshold}.pdf", bbox_inches="tight")
# save graph
results_path = f"data/graph_{threshold}.pkl"
with open(results_path, "wb") as f:
    pickle.dump(G_sub, f)
