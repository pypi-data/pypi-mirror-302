from typing import Iterable, Optional, Union, Literal
from typing_extensions import TypeAlias
import os

from .estimators import ESTIMATOR_REGISTRY, EstimatorBase
from .calculator import BDCalculator

VALID_METRICS_TYPE: TypeAlias = Literal["PSNR", "COV", "DIST", "GENERIC"]
VALID_METRICS = ["PSNR", "COV", "DIST", "GENERIC"]


def create_estimator(
    estimator_name,
    metric: Optional[str] = None,
    type: Union[Literal["quality", "rate"], None] = None,
    device: Literal["cpu", "cuda"] = "cpu",
) -> EstimatorBase:
    if estimator_name not in ESTIMATOR_REGISTRY:
        raise ValueError(f"Undefined BD estimator: {estimator_name}")

    if estimator_name == "neural":
        if metric is None:
            raise ValueError("Neural estimator requires a metric estimator_name!")
        if type not in ["quality", "rate"]:
            raise ValueError(
                "Neural estimator requires a metric type: 'quality' or 'rate'."
            )
        pretrained_model_path = os.path.join(
            os.path.split(__file__)[0], "neuralbd", "weights", f"{metric}-{type}"
        )
        return ESTIMATOR_REGISTRY[estimator_name](
            pretrained_model_path=pretrained_model_path, device=device
        )
    else:
        return ESTIMATOR_REGISTRY[estimator_name]()


def create_bd_calculator(
    estimator_name: str,
    metric: Optional[VALID_METRICS_TYPE] = None,
    device: Literal["cpu", "cuda"] = "cpu",
):
    estimator_rate = create_estimator(estimator_name, metric, "rate", device)
    estimator_quality = create_estimator(estimator_name, metric, "quality", device)
    return BDCalculator(estimator_rate, estimator_quality)


def BD_RATE(
    R1,
    D1,
    R2,
    D2,
    weight_group: VALID_METRICS_TYPE = "GENERIC",
    estimator_name="neural",
    device: Literal["cpu", "cuda"] = "cpu",
):
    bd_calculator = create_bd_calculator(estimator_name, weight_group, device)
    return bd_calculator.bd_rate(R1, D1, R2, D2)


def BD_QUALITY(
    R1,
    D1,
    R2,
    D2,
    weight_group: VALID_METRICS_TYPE = "GENERIC",
    estimator_name="neural",
    device: Literal["cpu", "cuda"] = "cpu",
):
    bd_calculator = create_bd_calculator(estimator_name, weight_group, device)
    return bd_calculator.bd_quality(R1, D1, R2, D2)


def BDCI_RATE(
    R1,
    D1,
    R2,
    D2,
    weight_group: VALID_METRICS_TYPE = "GENERIC",
    device: Literal["cpu", "cuda"] = "cpu",
    k=3,
):
    bd_calculator = create_bd_calculator("neural", weight_group, device)
    min, mean, max = bd_calculator.bd_rate_with_reliability(R1, D1, R2, D2, k=k)
    return min, max


def BDCI_QUALITY(
    R1,
    D1,
    R2,
    D2,
    weight_group: VALID_METRICS_TYPE = "GENERIC",
    device: Literal["cpu", "cuda"] = "cpu",
    k=3,
):
    bd_calculator = create_bd_calculator("neural", weight_group, device)
    min, mean, max = bd_calculator.bd_quality_with_reliability(R1, D1, R2, D2, k=k)
    return min, max
