from typing import Literal

import numpy as np
import torch
from tqdm import tqdm

from .segments import SegmentEstimatorBase


def generate_normalized_samples(x_in, y_in, x_bound=None):
    xmin, xmax, ymin, ymax = x_in.min(), x_in.max(), y_in.min(), y_in.max()

    # Normalize
    x_norm = (x_in - xmin) / (xmax - xmin)
    y_norm = (y_in - ymin) / (ymax - ymin)
    if x_bound is not None:
        x_bound = (x_bound - xmin) / (xmax - xmin)
    return x_norm, y_norm, x_bound


def make_dataset(
    segment_estimator: SegmentEstimatorBase,
    data_raw,
    num_samples,
    num_test_samples,
    type: Literal["quality", "rate"],
    min_interval,
    enable_tqdm=True,
):
    # build train dataset
    ds_in = []
    ds_out = []
    x_gts = []
    y_gts = []

    N = len(data_raw)

    for i in tqdm(range(num_samples + num_test_samples), desc="Building dataset"):
        sample = data_raw[i % N]

        r = sample.R
        d = sample.D
        lgr = np.log(r)

        if type == "quality":
            x = lgr
            y = d
        else:
            x = d
            y = lgr

        # Generate data samples
        x, y = np.sort(x), y[np.argsort(x)]

        if min_interval * 3 + 1 > len(sample):
            print(f"Sample #{i} too short. Skipped.")
            continue
        extra_interval_max = len(sample) - (min_interval * 3 + 1)
        extra_intervals_csum = np.sort(
            np.random.random_integers(0, extra_interval_max, 3)
        )
        extra_intervals_csum = np.concatenate([[0], extra_intervals_csum])
        start = np.random.random_integers(
            0, extra_interval_max - extra_intervals_csum[-1]
        )
        idx = start + np.arange(4) * min_interval + extra_intervals_csum
        x_in = x[idx]
        y_in = y[idx]

        xmin, xmax, ymin, ymax = x_in.min(), x_in.max(), y_in.min(), y_in.max()

        x_start = x_in[segment_estimator.pos]
        x_end = x_in[segment_estimator.pos + 1]

        # check bounded models
        if segment_estimator.dir != "None":
            x_bound = np.random.rand() * (x_end - x_start) + x_start
            if segment_estimator.dir == "left":
                x_start = x_bound
            else:
                x_end = x_bound
        else:
            x_bound = None

        # PCHIP estimate
        pchip_est = segment_estimator.pchip_estimator.estimate_integral(
            x_in, y_in, x_start, x_end
        )

        # Calculate difference
        gt = segment_estimator.pchip_estimator.estimate_integral(x, y, x_start, x_end)
        diff_norm = ((gt - pchip_est) / (x_end - x_start)) / (ymax - ymin)

        x_norm, y_norm, x_bound_norm = generate_normalized_samples(x_in, y_in, x_bound)

        # Save dataset
        if segment_estimator.dir != "None":
            ds_in.append(np.concatenate([x_norm, y_norm, [x_bound_norm]]))
        else:
            ds_in.append(np.concatenate([x_norm, y_norm]))
        ds_out.append(diff_norm)

        # Save ground truth metadata
        x_gt_norm = (x - xmin) / (xmax - xmin)
        y_gt_norm = (y - ymin) / (ymax - ymin)
        x_gts.append(x_gt_norm)
        y_gts.append(y_gt_norm)

    ds_in = torch.tensor(ds_in, dtype=torch.float32)
    ds_out = torch.tensor(ds_out, dtype=torch.float32)

    ds_in_train = ds_in[:-num_test_samples].cuda()
    ds_out_train = ds_out[:-num_test_samples].cuda()
    ds_in_test = ds_in[-num_test_samples:].cuda()
    ds_out_test = ds_out[-num_test_samples:].cuda()

    ds = {
        "train_input": ds_in_train,
        "train_label": ds_out_train,
        "test_input": ds_in_test,
        "test_label": ds_out_test,
        "x_gt": x_gts,
        "y_gt": y_gts,
    }

    return ds
