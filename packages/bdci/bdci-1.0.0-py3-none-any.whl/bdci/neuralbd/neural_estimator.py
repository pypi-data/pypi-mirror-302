import os
from typing import Dict, Iterable, Optional, Tuple

from ..estimators import EstimatorBase, PCHIPEstimator, register_estimator
from .data import generate_normalized_samples
from .segments import *

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WEIGHT_DIR = os.path.join(ROOTDIR, "weights")


@register_estimator("neural")
class NeuralEstimator(EstimatorBase):
    def __init__(
        self,
        net_type: NetType = "MLP",
        device="cpu",
        pretrained_model_path: Optional[str] = None,
    ):
        self.net_type = net_type
        self.estimators: Dict[str, SegmentEstimatorBase] = {
            "left": UnboundedLeft(net_type=net_type),
            "mid": UnboundedMid(net_type=net_type),
            "right": UnboundedRight(net_type=net_type),
            "leftb": BoundedLeft(net_type=net_type),
            "midleftb": BoundedMidLeft(net_type=net_type),
            "midrightb": BoundedMidRight(net_type=net_type),
            "rightb": BoundedRight(net_type=net_type),
        }

        self.pchip_interpolator = PCHIPEstimator()
        self.device = torch.device(device)

        if pretrained_model_path is not None:
            self.load_from_checkpoint(pretrained_model_path)

    def load_from_checkpoint(self, path: str):
        for name in self.estimators:
            self.estimators[name].load_from_checkpoint(
                os.path.join(path, f"{name}.pt"), prefix="net."
            )

    @torch.inference_mode()
    def estimate_segment(
        self,
        x_in,
        y_in,
        segment_estimator: SegmentEstimatorBase,
        x_bound: Optional[float] = None,
    ):
        xmin, xmax, ymin, ymax = x_in.min(), x_in.max(), y_in.min(), y_in.max()

        x_start = x_in[segment_estimator.pos]
        x_end = x_in[segment_estimator.pos + 1]

        if segment_estimator.dir != "None":
            if segment_estimator.dir == "left":
                x_start = x_bound
            else:
                x_end = x_bound

        # PCHIP estimate
        pchip_est = segment_estimator.pchip_estimator.estimate_integral(
            x_in, y_in, x_start, x_end
        )

        # Normalize
        x_norm, y_norm, x_bound_norm = generate_normalized_samples(x_in, y_in, x_bound)
        if segment_estimator.dir != "None":
            inp = np.concatenate([x_norm, y_norm, [x_bound_norm]], axis=0)
        else:
            inp = np.concatenate([x_norm, y_norm], axis=0)
        inp = torch.tensor(inp, device=self.device)

        mu, var = segment_estimator.forward(inp)

        mu = mu.detach().cpu().numpy()
        var = var.detach().cpu().numpy()

        est = pchip_est + mu * (ymax - ymin) * (x_end - x_start)
        var = var * ((ymax - ymin) * (x_end - x_start)) ** 2

        return est, var, pchip_est

    def estimate_integral_with_var(
        self,
        Xs: Iterable[float],
        Ys: Iterable[float],
        min_int: float,
        max_int: float,
        debug=False,
    ) -> Tuple[float, float]:
        if not len(Xs) == len(Ys):
            raise ValueError("Xs and Ys must have the same length.")

        if min_int > max_int:
            raise ValueError("min_int must be less than or equal to max_int.")

        if min_int < min(Xs):
            raise ValueError(
                "min_int must be greater than or equal to the minimum value in Xs."
            )

        if max_int > max(Xs):
            raise ValueError(
                "max_int must be less than or equal to the maximum value in Xs."
            )

        Xs, Ys = np.sort(Xs), Ys[np.argsort(Xs)]

        n = len(Xs)

        if n < 4:
            raise ValueError("must have at least 4 samples.")

        est_tot, var_tot, pchip_tot = 0, 0, 0

        for i in range(n - 1):
            x_left = Xs[i]
            x_right = Xs[i + 1]

            if x_right < min_int or x_left > max_int:
                continue
            elif min_int <= x_left and x_right <= max_int:
                if i == 0:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i : i + 4], Ys[i : i + 4], self.estimators["left"]
                    )
                elif i == n - 2:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i - 2 : i + 2], Ys[i - 2 : i + 2], self.estimators["right"]
                    )
                else:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i - 1 : i + 3], Ys[i - 1 : i + 3], self.estimators["mid"]
                    )
            elif x_left <= min_int and max_int <= x_right:
                raise ValueError(
                    f"min_int ~ max_int range is too narrow. Xs={Xs}; Ys={Ys}; min_int={min_int}; max_int={max_int}."
                )
            elif x_left <= min_int and min_int <= x_right:
                if i == 0:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i : i + 4], Ys[i : i + 4], self.estimators["leftb"], min_int
                    )
                elif i < n - 2:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i - 1 : i + 3],
                        Ys[i - 1 : i + 3],
                        self.estimators["midleftb"],
                        min_int,
                    )
                else:
                    raise ValueError(
                        f"min_int ~ max_int range is too narrow. Xs={Xs}; Ys={Ys}; min_int={min_int}; max_int={max_int}."
                    )
            elif x_left <= max_int and max_int <= x_right:
                if i == n - 2:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i - 2 : i + 2],
                        Ys[i - 2 : i + 2],
                        self.estimators["rightb"],
                        max_int,
                    )
                elif i >= 1:
                    est, var, pchip_est = self.estimate_segment(
                        Xs[i - 1 : i + 3],
                        Ys[i - 1 : i + 3],
                        self.estimators["midrightb"],
                        max_int,
                    )
                else:
                    raise ValueError(
                        f"min_int ~ max_int range is too narrow. Xs={Xs}; Ys={Ys}; min_int={min_int}; max_int={max_int}."
                    )
            if debug:
                print(
                    f"Segment {i}: {x_left}~{x_right}, est={est:.6f}, var={var:.6f}, pchip={pchip_est:.6f}"
                )
            est_tot += est
            var_tot += var
            pchip_tot += pchip_est

        return est_tot, var_tot, pchip_tot

    def estimate_integral(
        self, Xs: Iterable[float], Ys: Iterable[float], min_int: float, max_int: float
    ) -> float:
        try:
            mu, _, pchip_tot = self.estimate_integral_with_var(Xs, Ys, min_int, max_int)
        except ValueError:
            return self.pchip_interpolator.estimate_integral(Xs, Ys, min_int, max_int)
        return mu
