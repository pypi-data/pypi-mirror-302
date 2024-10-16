# Bjontegaard Delta - Confidence Interval

This repository contains the code used to compute the confidence intervals for classical Bjontegaard Delta.

## Installation

```
pip install bdci
```

## Basic Usages

```python
from bdci import BDCI_RATE

# R1 and D1 are the anchor

# Compute BDCI-rate (or BDCI-BR)
bdci_br_min, bdci_br_max = BDCI_RATE(R1, D1, R2, D2, metric_name='GENERIC')
# Compute BDCI-quality
bdci_quality_min, bdci_quality_max = BDCI_QUALITY(R1, D1, R2, D2, metric_name='GENERIC')
```

BDCI assumes that R1 and D1 are precise anchor. The confidence interval are only computed for R2 and D2.

## Select Proper Quality Metric Group

BDCI library provides 4 different weight groups corresponding to 4 different kinds of quality metrics. The corresponding weight groups are trained on specialized data for better accuracy. Use them to better improve the accuracy of BDCI. **The default setting should only be used when the quality metric is unknown or atypical.**

* `metric_name='PSNR_LIKE'`: Use when the quality metric is some kind of Signal-Noise-Ratio (SNR) that measured in dB. For example, PSNR, PSNR-HVS or PSNR-HVS-M.
* `metric_name='COV_LIKE`: Use when the quality metric is calculated using something like covariance, with a value range between -1 and 1, and the higher the better. For example, SSIM, MS-SSIM, IW-SSIM or FSIM.
* `metric_name='DIST_LIKE`: Use when the quality metric is a distance, with a value range between 0 and 1, and the lower the better. For example, LPIPS or RMSE.
* `metric_name='GENERIC'`: **(Default)** Use only when the quality metric is unknown or atypical.