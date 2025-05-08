import os
import pickle
import matplotlib.pyplot as plt
from omegaconf import OmegaConf
import numpy as np


def main(exp_name, save_path="plot_rank_c.pdf"):
    ### Load the configuration and results ###
    config_path = os.path.join("results", "outputs", exp_name, "config.yaml")
    config = OmegaConf.load(config_path)
    results_path = os.path.join("results", "outputs", exp_name, "results.pkl")
    with open(results_path, "rb") as f:
        results = pickle.load(f)
    mean_relative_error = results["mean_relative_error"]
    std_relative_error = results["std_relative_error"]
    horizon = config.experiment.horizon
    timesteps = np.arange(horizon)
    ### End of loading ###

    ### Plot config ###
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    fontsize = 12
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 10,
        }
    )
    colors = ["C0", "C1", "C7"]
    markers = ["^", "o", "s"]
    ### End of plot config ###

    for name, color, marker in zip(mean_relative_error.keys(), colors, markers):
        print(name)
        ax.plot(
            timesteps,
            mean_relative_error[name],
            marker=marker,
            color=color,
            label=name,
            markevery=range(horizon // 10, horizon, horizon // 10),
            markersize=6,
        )
        ax.fill_between(
            timesteps,
            mean_relative_error[name] - std_relative_error[name],
            mean_relative_error[name] + std_relative_error[name],
            color=color,
            alpha=0.3,
        )

    ax.set_ylim(0.0, 0.5)
    ax.set_xlim(0, horizon)
    ticks = np.linspace(0, horizon, 5, dtype=int)
    ax.set_xticks(ticks)
    ax.set_xticklabels([0] + [f"{t/1e4:.0f}e4" for t in ticks[1:]])
    ax.set_yticks(np.linspace(0, 0.5, 6))
    plt.title("Absolute Error vs. Timesteps", fontsize=fontsize)
    plt.legend()
    plot_path = os.path.join("results", "figures", save_path)
    plt.savefig(plot_path, format="pdf", bbox_inches="tight")
    plt.show()
