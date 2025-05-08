import numpy as np
from abc import ABC
from src.utils import wn


class MeanEstimate(ABC):
    def __init__(self, horizon, n, data, alpha, rank_class):
        self.horizon = horizon
        self.n = n
        self.alpha = alpha
        self.data = data.copy()
        self.historical_z = np.zeros((horizon, n))
        self.historical_avg = np.zeros((horizon, n))
        self.historical_w = np.zeros((horizon, n))
        self.rank = rank_class(horizon, n, data)
        self.weight = self.rank.weight * n
        self.name = "GoTrim + " + self.rank.name

    def update_mean(self, t, i, j):
        # update dynamic weights
        self.historical_w[t] = self.n * wn(
            self.n, self.weight * self.rank.historical_ranking[t] + 1, self.alpha
        )

        # update z estimate of all nodes
        delta = self.historical_w[t] - self.historical_w[t - 1]
        self.historical_z[t - 1] = self.historical_z[t - 1] + delta * self.data

        # update z estimate for nodes i, j
        self.historical_z[t] = self.historical_z[t - 1].copy()
        self.historical_z[t][i] = (
            self.historical_z[t - 1][i] + self.historical_z[t - 1][j]
        ) / 2
        self.historical_z[t][j] = (
            self.historical_z[t - 1][i] + self.historical_z[t - 1][j]
        ) / 2


class ClippedGossip(ABC):
    def __init__(self, horizon, n, data, tau):
        self.horizon = horizon
        self.n = n
        self.tau = tau
        self.data = data.copy()
        self.historical_z = np.zeros((horizon, n))
        self.historical_z[0] = data.copy()
        self.name = "Clipped Gossip (He et al.)"

    def clip(self, z, tau):
        norm = np.linalg.norm(z)
        factor = min(1, tau / norm) if norm > 0 else 1
        return factor * z

    def update_mean(self, t, i, j):
        xi_prev = self.historical_z[t - 1][i]
        xj_prev = self.historical_z[t - 1][j]

        delta = xj_prev - xi_prev
        clipped_delta = self.clip(delta, self.tau)

        self.historical_z[t] = self.historical_z[t - 1].copy()
        self.historical_z[t][i] = xi_prev + 0.5 * clipped_delta
        self.historical_z[t][j] = xj_prev - 0.5 * clipped_delta
