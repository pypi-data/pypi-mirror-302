import abc
from typing import Iterable, Optional

import numpy as np

from .neuralbd.neural_estimator import NeuralEstimator

from .estimators import EstimatorBase


class BDCalculator:
    def __init__(
        self,
        estimator: EstimatorBase,
        quality_estimator: Optional[EstimatorBase] = None,
    ):
        self.rate_estimator = estimator
        if quality_estimator is not None:
            self.quality_estimator = quality_estimator
        else:
            self.quality_estimator = estimator

    def to_numpy(self, x):
        return np.asanyarray(x, dtype=np.float32)

    def bd_rate(
        self,
        R1: Iterable[float],
        D1: Iterable[float],
        R2: Iterable[float],
        D2: Iterable[float],
    ) -> float:
        """
        calculate the BD-rate. 1 is the anchor
        """

        R1 = self.to_numpy(R1)
        D1 = self.to_numpy(D1)
        R2 = self.to_numpy(R2)
        D2 = self.to_numpy(D2)

        lR1 = np.log(R1)
        lR2 = np.log(R2)

        min_int = max(min(D1), min(D2))
        max_int = min(max(D1), max(D2))

        int1 = self.rate_estimator.estimate_integral(D1, lR1, min_int, max_int)
        int2 = self.rate_estimator.estimate_integral(D2, lR2, min_int, max_int)

        avg_exp_diff = (int2 - int1) / (max_int - min_int)
        avg_diff = (np.exp(avg_exp_diff) - 1) * 100
        return avg_diff

    def bd_quality(
        self,
        R1: Iterable[float],
        D1: Iterable[float],
        R2: Iterable[float],
        D2: Iterable[float],
    ) -> float:
        """
        calculate the BD-quality. 1 is the anchor
        """
        R1 = self.to_numpy(R1)
        D1 = self.to_numpy(D1)
        R2 = self.to_numpy(R2)
        D2 = self.to_numpy(D2)

        lR1 = np.log(R1)
        lR2 = np.log(R2)

        min_int = max(min(lR1), min(lR2))
        max_int = min(max(lR1), max(lR2))

        int1 = self.quality_estimator.estimate_integral(lR1, D1, min_int, max_int)
        int2 = self.quality_estimator.estimate_integral(lR2, D2, min_int, max_int)

        avg_diff = (int2 - int1) / (max_int - min_int)
        return avg_diff

    def bd_rate_with_reliability(
        self,
        R1: Iterable[float],
        D1: Iterable[float],
        R2: Iterable[float],
        D2: Iterable[float],
        k: float = 3.0,
        debug=False,
    ):
        if not (hasattr(self.rate_estimator, "estimate_integral_with_var")):
            raise ValueError("Requires rate estimator to support prob estimation.")

        self.rate_estimator: NeuralEstimator = self.rate_estimator

        R1 = self.to_numpy(R1)
        D1 = self.to_numpy(D1)
        R2 = self.to_numpy(R2)
        D2 = self.to_numpy(D2)

        lR1 = np.log(R1)
        lR2 = np.log(R2)

        min_int = max(min(D1), min(D2))
        max_int = min(max(D1), max(D2))

        int1 = self.rate_estimator.estimate_integral(D1, lR1, min_int, max_int)
        int2, var, _ = self.rate_estimator.estimate_integral_with_var(
            D2, lR2, min_int, max_int, debug=debug
        )

        int2_wr_max = int2 + np.sqrt(var) * k
        int2_wr_min = int2 - np.sqrt(var) * k

        avg_exp_diff_max = (int2_wr_max - int1) / (max_int - min_int)
        avg_exp_diff_min = (int2_wr_min - int1) / (max_int - min_int)
        avg_exp_diff_est = (int2 - int1) / (max_int - min_int)
        avg_diff_max = (np.exp(avg_exp_diff_max) - 1) * 100
        avg_diff_min = (np.exp(avg_exp_diff_min) - 1) * 100
        avg_diff_est = (np.exp(avg_exp_diff_est) - 1) * 100
        return avg_diff_min, avg_diff_est, avg_diff_max

    def bd_quality_with_reliability(
        self,
        R1: Iterable[float],
        D1: Iterable[float],
        R2: Iterable[float],
        D2: Iterable[float],
        k: float = 3.0,
    ):
        if not (hasattr(self.quality_estimator, "estimate_integral_with_var")):
            raise ValueError("Requires quality estimator to support prob estimation.")

        self.quality_estimator: NeuralEstimator = self.quality_estimator

        R1 = self.to_numpy(R1)
        D1 = self.to_numpy(D1)
        R2 = self.to_numpy(R2)
        D2 = self.to_numpy(D2)

        lR1 = np.log(R1)
        lR2 = np.log(R2)

        min_int = max(min(lR1), min(lR2))
        max_int = min(max(lR1), max(lR2))

        int1 = self.quality_estimator.estimate_integral(lR1, D1, min_int, max_int)
        int2, var, _ = self.quality_estimator.estimate_integral_with_var(
            lR2, D2, min_int, max_int
        )

        int2_wr_max = int2 + np.sqrt(var) * k
        int2_wr_min = int2 - np.sqrt(var) * k

        avg_diff_max = (int2_wr_max - int1) / (max_int - min_int)
        avg_diff_min = (int2_wr_min - int1) / (max_int - min_int)
        avg_diff_est = (int2 - int1) / (max_int - min_int)
        return avg_diff_min, avg_diff_est, avg_diff_max
