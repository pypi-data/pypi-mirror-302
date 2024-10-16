import os
import random
from dataclasses import dataclass
from typing import Literal

import numpy as np
import torch
from genericpath import isfile
from transformers.hf_argparser import HfArgumentParser

from bdlib.estimators import PCHIPEstimator
from bdlib.neuralbd.data import make_dataset
from bdlib.neuralbd.neural_estimator import NeuralEstimator
from bdlib.neuralbd.segments import BoundedEstimatorBase, UnboundedEstimatorBase
from bdlib.neuralbd.train_utils import get_ckpt_folder
from bdlib.neuralbd.types import NetType
from RD120K_tools.dataset import RD120K_Train


@dataclass
class TrainArgs:
    dataset_dir: str
    metric: str
    submodel_name: Literal[
        "left", "mid", "right", "leftb", "midleftb", "midrightb", "rightb"
    ]
    type: Literal["quality", "rate"]
    net_type: NetType = "MLP"
    train_steps: int = 100
    num_rd_samples: int = 1000000
    test_batch_size: int = 20000
    min_interval: int = 3
    seed: int = 19260817
    skip_if_exists: bool = False
    learning_rate: float = 0.001


def set_seed(seed_value):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)


def parse_args() -> TrainArgs:
    parser = HfArgumentParser(TrainArgs)
    args: TrainArgs = parser.parse_args()
    return args


def main(args: TrainArgs):
    print(f"Args: {args}")
    ckpt_folder = get_ckpt_folder(args.metric, args.type)
    os.makedirs(ckpt_folder, exist_ok=True)
    ckpt_filename = os.path.join(ckpt_folder, args.submodel_name + ".pt")

    print(f"Checkpoint path: {ckpt_filename}")
    if os.path.isfile(ckpt_filename) and args.skip_if_exists:
        print(f'Checkpoint "{ckpt_filename}" already exists, skipping training')
        return

    estimator = NeuralEstimator(args.net_type, pretrained_model_path=None)
    model = estimator.estimators[args.submodel_name]

    data_raw = RD120K_Train(args.dataset_dir, metric=args.metric)
    dataset = make_dataset(
        model,
        data_raw,
        num_samples=args.num_rd_samples,
        num_test_samples=args.test_batch_size,
        type=args.type,
        min_interval=args.min_interval,
    )

    model.train_net(dataset, steps=args.train_steps, learning_rate=args.learning_rate)

    torch.save(model.state_dict(), ckpt_filename)


if __name__ == "__main__":
    args = parse_args()
    print(__file__, ": Args:", args)
    set_seed(args.seed)
    main(args)
