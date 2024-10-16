import os
from abc import ABC, abstractmethod
from typing import Dict, Literal, Optional

import numpy as np
import scipy.interpolate as interp
import torch
import torch.nn as nn
from torch.distributions import Dirichlet, Laplace, Normal

from ..estimators import PCHIPEstimator
from .mlp_with_trainer import MLPWithTrainer
from .types import NetType


def mle_loss(x, gt):
    mus = (x[:, 0] - 1) / 100
    # logstd = x[:, [1]] * 8 - 6
    logstd = x[:, 1]

    gt0 = (gt - mus) / torch.exp(logstd)
    D = Normal(0, 1)
    # p = D.prob(gt0) / sigmas
    lgp = D.log_prob(gt0) - logstd
    loss = torch.mean(-lgp)
    return loss


class SegmentEstimatorBase(nn.Module, ABC):
    def __init__(self, net_type: NetType, n_in: int, *args, **kwargs) -> None:
        super().__init__()
        self.pchip_estimator = PCHIPEstimator()
        self.bounded: bool = False
        self.dir: Literal[
            "left", "right", "None"
        ] = "None"  # dir = 'left' means the bound is the left end
        self.segment: Literal["left", "mid", "right"] = None

        if net_type == "MLP":
            self.net = MLPWithTrainer(n_in, 128, 2, 6)
        else:
            raise ValueError(f"Unrecognized net type: {net_type}")

    def train_net(
        self,
        dataset,
        *,
        steps: int = 100,
        learning_rate: float = 1e-3,
        decay_rate: float = 1e-3 ** (1.0 / 1000),
    ):
        """
        inputs: [T, 8], (x1, x2, x3, x4, y1, y2, y3, y4, x_bound)
        gts: [T, 1]
        仅用于求积分，log需要在输入该函数之前求
        """

        """
        inputs: [T, 8], (x1, x2, x3, x4, y1, y2, y3, y4)
        gts: [T, 1]
        仅用于求积分，log需要在输入该函数之前求
        """

        lr = learning_rate
        self.net.cuda()

        print("Trainable Parameters:", sum(p.numel() for p in self.net.parameters()))
        print("Total Parameters:", sum(p.numel() for p in self.net.parameters()))

        ds_in_test = dataset["test_input"]
        ds_out_test = dataset["test_label"]

        best_val_loss = None
        best_weights = None

        for i in range(steps):
            train_loss = self.net.train(
                dataset,
                steps=1,
                loss_fn=mle_loss,
                lr=lr,
                lamb_l1=0,
                lamb_entropy=0,
                device="cuda",
                opt="LBFGS",
            )

            output = self.net(ds_in_test)
            gts = ds_out_test
            val_loss = mle_loss(output, gts)

            if best_val_loss is None or val_loss < best_val_loss:
                best_val_loss = val_loss
                best_weights = self.net.state_dict()

            mu_full = (output[:, 0].detach() - 1) / 100
            mu = mu_full[0]
            logstd = output[0, 1]
            std = torch.exp(logstd)
            gt = gts[0].detach()
            # pchip_ested = ds_in_test[0, 8]
            pchip_ested = 0

            print(
                f"\nStep {i}: lr={lr} | mu={mu}; logstd={logstd}; pchip_ested={pchip_ested}; gt={gt}; sigma={std}; -3sigma={mu-3*std}; +3sigma={mu+3*std}"
            )
            print(f"Train_loss={train_loss:.5f}; Test_loss={val_loss:.5f}")

            mse_pchip = torch.mean(gts**2)
            mse_est = torch.mean((gts - mu_full) ** 2)
            print(f"mse_pchip={mse_pchip}; mse_ours={mse_est}")

            lr *= decay_rate

        self.net.load_state_dict(best_weights)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        self.to(x.device)
        x = x.unsqueeze(0)
        y = self.net(x)
        mu = (y[0, 0] - 1.0) / 100.0
        logstd = y[0, 1]
        var = torch.exp(logstd * 2)
        return mu, var

    def load_from_checkpoint(self, path: str, prefix: Optional[str] = None) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Checkpoint {path} does not exist.")
        ckpt: Dict = torch.load(path, map_location="cpu")

        ckpt2 = {}

        for k, v in ckpt.items():
            if prefix is not None and k.startswith(prefix):
                ckpt2[k[len(prefix) :]] = v
            else:
                ckpt2[k] = v
        self.net.load_state_dict(ckpt2)


class UnboundedEstimatorBase(SegmentEstimatorBase):
    def __init__(self, *, net_type: NetType, pos=0, **kwargs) -> None:
        super().__init__(net_type=net_type, n_in=8, **kwargs)
        self.pos = pos


class UnboundedLeft(UnboundedEstimatorBase):
    def __init__(self, net_type: NetType, *args, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=0, *args, **kwargs)


class UnboundedMid(UnboundedEstimatorBase):
    def __init__(self, net_type: NetType, *args, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=1, *args, **kwargs)


class UnboundedRight(UnboundedEstimatorBase):
    def __init__(self, net_type: NetType, *args, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=2, *args, **kwargs)


class BoundedEstimatorBase(SegmentEstimatorBase):
    def __init__(
        self, *, net_type: NetType, pos=0, dir: Literal["left", "right"], **kwargs
    ) -> None:
        super().__init__(net_type=net_type, n_in=9, **kwargs)
        self.pos = pos
        self.dir: Literal["left", "right"] = dir


class BoundedLeft(BoundedEstimatorBase):
    def __init__(self, net_type: NetType, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=0, dir="left", **kwargs)


class BoundedMidLeft(BoundedEstimatorBase):
    def __init__(self, net_type: NetType, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=1, dir="left", **kwargs)


class BoundedMidRight(BoundedEstimatorBase):
    def __init__(self, net_type: NetType, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=1, dir="right", **kwargs)


class BoundedRight(BoundedEstimatorBase):
    def __init__(self, net_type: NetType, **kwargs) -> None:
        super().__init__(net_type=net_type, pos=2, dir="right", **kwargs)
