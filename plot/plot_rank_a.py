import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from omegaconf import OmegaConf


def main(exp_name, save_path="plot_rank_a.pdf"):
    ### Load the configuration and results ###
    config_path = os.path.join("results", "outputs", exp_name, "config.yaml")
    config = OmegaConf.load(config_path)
    results_path = os.path.join("results", "outputs", exp_name, "results.pkl")
    with open(results_path, "rb") as f:
        results = pickle.load(f)
    true_ranks = results["true_ranks"]
    error_mean = results["error_mean"]
    names = results["names"]
    n = config.data.n
    ### End of loading ###

    ### Plot configuration ###
    fontsize = 12
    plt.rcParams.update(
        {
            "font.size": 10,  # Base font size
            "axes.labelsize": 10,  # Axis label size
            "axes.titlesize": 12,  # Title size
            "xtick.labelsize": 10,  # X tick label size
            "ytick.labelsize": 10,  # Y tick label size
            "legend.fontsize": 10,  # Legend font size
        }
    )
    ### End of plot configuration ###

    def sigma_n(r, n):
        x = r / n
        return np.sqrt(x * (1 - x))

    theo_shape = sigma_n(true_ranks, n)
    name = names[0]
    fig, ax1 = plt.subplots(figsize=(3.2, 3.0))
    line1 = ax1.scatter(
        true_ranks + 1, error_mean[name], label="GoRank", color="C1", marker="^", s=15
    )
    ax1.tick_params(axis="y", labelcolor="C1")
    ax1.set_xticks(np.linspace(0, n, 5, dtype=int))
    max_error = np.round(np.max(error_mean[name]), 2)
    ax1.set_yticks(np.round(np.linspace(0, max_error, 5), 2))
    ax2 = ax1.twinx()
    line2 = ax2.scatter(
        true_ranks + 1, theo_shape, label="Bound", color="C7", marker="o", s=10
    )
    ax2.tick_params(axis="y", labelcolor="C7")
    ax2.set_yticks(np.round(np.linspace(0, 0.5, 3), 2))
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    fig.legend(lines, labels, loc="upper center", bbox_to_anchor=(0.5, 0.35))
    plt.title("Absolute Error vs. Rank", fontsize=fontsize)
    plot_path = os.path.join("results", "figures", save_path)
    plt.savefig(plot_path, format="pdf", bbox_inches="tight")
    plt.show()
