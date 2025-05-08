import numpy as np
from abc import ABC, abstractmethod


class RankEstimate(ABC):
    """
    Abstract class for ranking estimates.
    """

    def __init__(self, horizon, n, data):
        self.horizon = horizon
        self.n = n
        self.data = data.copy()
        self.historical_ranking = np.zeros((horizon, n))
        self.name = "Ranking"

    @abstractmethod
    def update(self, t, i, j):
        pass


class GoRankEstimate(RankEstimate):
    """
    This class implements the GoRank algorithm
    """

    def __init__(self, horizon, n, data):
        super().__init__(horizon, n, data)
        self.y_data = data.copy()
        self.weight = 1
        self.color = "C1"
        self.name = "GoRank (ours)"
        self.marker = "C1o-"

    def update(self, t, i, j):
        # Update auxiliary rank estimates
        self.historical_ranking[t] = (t - 1) * self.historical_ranking[t - 1]
        self.historical_ranking[t] += self.data > self.y_data
        self.historical_ranking[t] /= t
        # Swap auxiliary observations
        self.y_data[[i, j]] = self.y_data[[j, i]]


class ImprovedBaselineEstimate(RankEstimate):
    """
    This class implements the Baseline++ algorithm
    """

    def __init__(self, horizon, n, data):
        super().__init__(horizon, n, data)
        self.historical_aux_r = np.zeros((horizon, n))
        self.historical_aux_x = np.zeros((horizon, n))
        self.historical_ranking[0] = np.arange(n)
        self.historical_aux_r[0] = np.arange(n)
        self.historical_aux_x[0] = data.copy()
        self.weight = 1 / n
        self.color = "b"
        self.name = "Baseline++ (ours)"

    def update(self, t, i, j):
        self.historical_ranking[t] = self.historical_ranking[t - 1].copy()
        self.historical_aux_r[t] = self.historical_aux_r[t - 1].copy()
        self.historical_aux_x[t] = self.historical_aux_x[t - 1].copy()

        # If auxiliary rankins contradicts auxiliary observations, swap
        predicted_diff = self.historical_aux_r[t][i] - self.historical_aux_r[t][j]
        truth_diff = self.historical_aux_x[t][i] - self.historical_aux_x[t][j]
        if truth_diff * predicted_diff < 0:
            self.historical_aux_r[t][i], self.historical_aux_r[t][j] = (
                self.historical_aux_r[t - 1][j],
                self.historical_aux_r[t - 1][i],
            )

        # Update local rank with auxiliary rank if there is a contradiction
        for node in [i, j]:
            predicted_diff = (
                self.historical_ranking[t][node] - self.historical_aux_r[t][node]
            )
            truth_diff = self.data[node] - self.historical_aux_x[t][node]

            # Update local rank
            if truth_diff * predicted_diff < 0 or truth_diff == 0:
                self.historical_ranking[t][node] = self.historical_aux_r[t][node]

        # Swap auxiliary variables
        self.historical_aux_r[t][i], self.historical_aux_r[t][j] = (
            self.historical_aux_r[t][j],
            self.historical_aux_r[t][i],
        )
        self.historical_aux_x[t][i], self.historical_aux_x[t][j] = (
            self.historical_aux_x[t][j],
            self.historical_aux_x[t][i],
        )


class BaselineEstimate(RankEstimate):
    """
    This class implements the Baseline++ algorithm
    """

    def __init__(self, horizon, n, data):
        super().__init__(horizon, n, data)
        self.historical_aux_r = np.zeros((horizon, n))
        self.historical_aux_x = np.zeros((horizon, n))
        self.historical_aux_i = np.zeros((horizon, n))
        self.historical_ranking[0] = np.arange(n)
        self.historical_aux_r[0] = np.arange(n)
        self.historical_aux_x[0] = data.copy()
        self.historical_aux_i[0] = range(n)
        self.weight = 1 / n
        self.color = "green"
        self.name = "Baseline (Chiuso et al.)"

    def update(self, t, i, j):
        self.historical_ranking[t] = self.historical_ranking[t - 1].copy()
        self.historical_aux_r[t] = self.historical_aux_r[t - 1].copy()
        self.historical_aux_x[t] = self.historical_aux_x[t - 1].copy()
        self.historical_aux_i[t] = self.historical_aux_i[t - 1].copy()

        # Swap rankings if necessary
        if (self.data[i] - self.data[j]) * (
            self.historical_ranking[t - 1][i] - self.historical_ranking[t - 1][j]
        ) < 0:
            self.historical_ranking[t][i], self.historical_ranking[t][j] = (
                self.historical_ranking[t - 1][j],
                self.historical_ranking[t - 1][i],
            )

        # Swap auxiliary rankings if necessary
        if (self.historical_aux_x[t - 1][i] - self.historical_aux_x[t - 1][j]) * (
            self.historical_aux_r[t - 1][i] - self.historical_aux_r[t - 1][j]
        ) < 0:
            self.historical_aux_r[t][i], self.historical_aux_r[t][j] = (
                self.historical_aux_r[t - 1][j],
                self.historical_aux_r[t - 1][i],
            )

        # Swap auxiliary variables
        self.historical_aux_i[t][i], self.historical_aux_i[t][j] = (
            self.historical_aux_i[t][j],
            self.historical_aux_i[t][i],
        )
        self.historical_aux_r[t][i], self.historical_aux_r[t][j] = (
            self.historical_aux_r[t][j],
            self.historical_aux_r[t][i],
        )
        self.historical_aux_x[t][i], self.historical_aux_x[t][j] = (
            self.historical_aux_x[t][j],
            self.historical_aux_x[t][i],
        )

        # Update local ranking estimates
        for p in [i, j]:
            if self.historical_aux_i[t][p] == p:
                self.historical_ranking[t][p] = self.historical_aux_r[t][p]
