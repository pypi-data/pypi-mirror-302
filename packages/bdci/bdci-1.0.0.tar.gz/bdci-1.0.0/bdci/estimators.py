import abc
from typing import Dict, Iterable, Type

import numpy as np
import scipy.interpolate as interp


class EstimatorBase(abc.ABC):
    @abc.abstractmethod
    def estimate_integral(
        self, Xs: Iterable[float], Ys: Iterable[float], min_int: float, max_int: float
    ) -> float:
        """
        Estimates the integral of a function over a set of points.
        """


ESTIMATOR_REGISTRY: Dict[str, Type[EstimatorBase]] = {}


def register_estimator(name: str):
    def decorator(cls):
        ESTIMATOR_REGISTRY[name] = cls
        return cls

    return decorator


@register_estimator("cubic")
class CubicEstimator(EstimatorBase):
    def estimate_integral(
        self, Xs: Iterable[float], Ys: Iterable[float], min_int: float, max_int: float
    ) -> float:
        """
        Estimates the integral of a function over a set of points.
        """
        Xs, Ys = np.sort(Xs), Ys[np.argsort(Xs)]
        p = np.polyfit(Xs, Ys, 3)
        ans = np.polyval(p, max_int) - np.polyval(p, min_int)
        return ans


@register_estimator("csi")
class CSIEstimator(EstimatorBase):
    def estimate_integral(
        self, Xs: Iterable[float], Ys: Iterable[float], min_int: float, max_int: float
    ) -> float:
        lin = np.linspace(min_int, max_int, num=1000, retstep=True)
        interval = lin[1]
        samples = lin[0]
        Xs, Ys = np.sort(Xs), Ys[np.argsort(Xs)]

        interpolator = interp.CubicSpline(Xs, Ys)

        v = interpolator(samples)
        ans = np.trapz(v, dx=interval)
        return ans


@register_estimator("pchip")
class PCHIPEstimator(EstimatorBase):
    def estimate_integral(
        self, Xs: Iterable[float], Ys: Iterable[float], min_int: float, max_int: float
    ) -> float:
        """
        Estimates the integral of a function over a set of points.
        """
        Xs, Ys = np.sort(Xs), Ys[np.argsort(Xs)]
        lin = np.linspace(min_int, max_int, num=1000, retstep=True)
        interval = lin[1]
        samples = lin[0]

        v = interp.pchip_interpolate(np.sort(Xs), Ys[np.argsort(Xs)], samples)
        ans = np.trapz(v, dx=interval)
        return ans


@register_estimator("akima")
class AkimaEstimator(EstimatorBase):
    def estimate_integral(
        self, Xs: Iterable[float], Ys: Iterable[float], min_int: float, max_int: float
    ) -> float:
        lin = np.linspace(min_int, max_int, num=1000, retstep=True)
        interval = lin[1]
        samples = lin[0]

        Xs, Ys = np.sort(Xs), Ys[np.argsort(Xs)]

        interpolator = interp.Akima1DInterpolator(Xs, Ys)

        v = interpolator(samples)
        ans = np.trapz(v, dx=interval)
        return ans
