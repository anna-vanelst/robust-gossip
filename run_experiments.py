import random
import numpy as np
from src.graph import generate_graph
from scipy.stats import trim_mean
from src.rank import (
    GoRankEstimate,
    ImprovedBaselineEstimate,
    BaselineEstimate,
    GoRankEstimateAsync,
)
from src.trim import MeanEstimate, ClippedGossip
import os
import pickle
from omegaconf import OmegaConf
import yaml
from src.utils import wn, compute_connectivity
import argparse
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp_name", type=str, default="", help="Name of the experiment"
    )
    args = parser.parse_args()
    exp_name = args.exp_name

    ### CONFIG ###
    config_path = os.path.join("configs", f"{exp_name}.yaml")
    config = OmegaConf.load(config_path)
    exp_name = config.path.folder
    print(f"Running experiment: {exp_name}")
    n = config.data.n
    if config.data.type == "arange":
        data = np.arange(1, n + 1)
        eps = OmegaConf.select(config, "data.eps") or 0
        n_outliers = int(eps * n)
        if n_outliers > 0:
            # scale contamination
            outlier = OmegaConf.select(config, "data.outlier") or 10
            indices = np.random.choice(n, n_outliers, replace=False)
            data[indices] = outlier * data[indices]
        graph_init = False
    elif config.data.type == "real":
        treshold = OmegaConf.select(config, "data.treshold") or 0
        file = f"data/graph_{treshold}.pkl"
        with open(file, "rb") as f:
            graph = pickle.load(f)
            print(f"Connectivity: {compute_connectivity(graph):.2e}")
            graph_init = True
        data = np.array([graph.nodes[i]["temperature"] for i in graph.nodes()])
        eps = OmegaConf.select(config, "data.eps") or 0
        n = len(data)
        print("Dataset size", n)
        n_outliers = int(eps * n)
        print("Normal data", np.mean(data))
        if n_outliers > 0:
            # randomly select n_outliers indices to corrupt
            indices = np.random.choice(n, n_outliers, replace=False)
            outlier = OmegaConf.select(config, "data.outlier") or 100
            data[indices] = data[indices] + outlier  # shift contamination
        # add small noise to make sure data is disctinct
        data = np.array([v + random.uniform(-1e-4, 1e-4) for v in data])
    else:
        print("Wrong data type.")
    n_trials = config.experiment.n_trials
    horizon = config.experiment.horizon
    graph_type = config.graph
    alpha = OmegaConf.select(config, "trimming.alpha") or 0
    task = OmegaConf.select(config, "task") or "ranking"
    shuffle = OmegaConf.select(config, "data.shuffle") or "yes"
    seed = config.experiment.seed
    if config.ranking == "GoRank":
        class_estimates = [GoRankEstimate]
    elif config.ranking == "All":
        class_estimates = [GoRankEstimate, ImprovedBaselineEstimate, BaselineEstimate]
    elif config.ranking == "Async":
        class_estimates = [
            ImprovedBaselineEstimate,
            GoRankEstimate,
            GoRankEstimateAsync,
        ]
    ### END CONDIG ###

    ### INIT ###
    np.random.seed(seed)
    np.random.shuffle(data)
    true_ranks = np.argsort(np.argsort(data))
    trimmed_mean = trim_mean(data, alpha)
    print("Corrupted mean", np.mean(data))
    print("Robust mean", trimmed_mean)
    true_value = np.full(n, trimmed_mean)
    if not graph_init:
        graph = generate_graph(n=n, type=graph_type, seed=seed)
        print(f"Connectivity: {compute_connectivity(graph):.2e}")
    edges = list(graph.edges)
    if task == "ranking":
        estimates = [
            class_estimate(horizon, n, data) for class_estimate in class_estimates
        ]
    elif task == "averaging":
        class_estimates = [GoRankEstimate, ImprovedBaselineEstimate]
        estimates = [
            MeanEstimate(horizon, n, data, alpha, rank_class)
            for rank_class in class_estimates
        ]
        tau = OmegaConf.select(config, "clipping.tau") or 100
        estimates += [ClippedGossip(horizon, n, data, tau)]
    error_mean = {estimate.name: np.zeros(n) for estimate in estimates}
    all_relative_errors = {estimate.name: [] for estimate in estimates}
    ### END INIT ###

    ### SCRIPT ###
    for trial in range(n_trials):
        if shuffle == "yes":
            np.random.shuffle(data)
            true_ranks = np.argsort(np.argsort(data))
        if trial % 10 == 0:
            print(f"Trial {trial}/{n_trials}")
        if task == "ranking":
            estimates = [
                class_estimate(horizon, n, data) for class_estimate in class_estimates
            ]
        elif task == "averaging":
            estimates = [
                MeanEstimate(horizon, n, data, alpha, rank_class)
                for rank_class in class_estimates
            ]
            estimates += [ClippedGossip(horizon, n, data, tau)]
        t = 1
        while t < horizon:
            i, j = random.choice(edges)
            for estimate in estimates:
                if task == "ranking":
                    estimate.update(t, i, j)

                elif task == "averaging":
                    if "Clipped Gossip" not in estimate.name:
                        estimate.rank.update(t, i, j)
                    estimate.update_mean(t, i, j)
            t += 1
        relative_error = {estimate.name: np.zeros(horizon) for estimate in estimates}
        for estimate in estimates:
            if task == "ranking":
                estimated_ranks = estimate.historical_ranking[-1] * estimate.weight
                absolute_error = np.abs(estimated_ranks - (true_ranks / n))
                error_mean[estimate.name] += absolute_error
                for t in range(horizon):
                    estimated_ranks = estimate.historical_ranking[t] * estimate.weight
                    relative_error[estimate.name][t] = np.average(
                        np.abs(estimated_ranks - (true_ranks / n))
                    )
                all_relative_errors[estimate.name].append(relative_error[estimate.name])
            elif task == "averaging":
                true_weight = n * wn(n, true_ranks + 1, alpha)
                if "Clipped Gossip" not in estimate.name:
                    absolute_error = np.abs(estimate.historical_w[-1] - true_weight)
                    error_mean[estimate.name] += absolute_error
                for t in range(horizon):
                    relative_error[estimate.name][t] = np.average(
                        np.abs(estimate.historical_z[t] - true_value)
                    )
                all_relative_errors[estimate.name].append(relative_error[estimate.name])

    for estimate in estimates:
        error_mean[estimate.name] /= n_trials
        mean_relative_error = {
            estimate.name: np.mean(all_relative_errors[estimate.name], axis=0)
            for estimate in estimates
        }
        std_relative_error = {
            estimate.name: np.std(all_relative_errors[estimate.name], axis=0)
            for estimate in estimates
        }
    names = [estimate.name for estimate in estimates]
    ### SCRIPT ###

    ### SAVE ###
    results = {
        "names": names,
        "config": config,
        "data": data,
        "true_ranks": true_ranks,
        "error_mean": error_mean,
        "mean_relative_error": mean_relative_error,
        "std_relative_error": std_relative_error,
    }
    folder_name = config.path.folder
    path = os.path.join("results", "outputs", folder_name)
    os.makedirs(path, exist_ok=True)
    config_path = os.path.join(path, "config.yaml")
    results_path = os.path.join(path, config.path.output)
    with open(results_path, "wb") as f:
        pickle.dump(results, f)
    config_dict = OmegaConf.to_container(config, resolve=True)
    with open(config_path, "w") as f:
        yaml.dump(config_dict, f, sort_keys=False)
    ### END SAVE ###


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Execution time: {(end - start) / 60:.2} minutes")
