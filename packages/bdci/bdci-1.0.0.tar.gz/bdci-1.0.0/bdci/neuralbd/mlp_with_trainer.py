from typing import Any, Dict

import torch
import torch.nn as nn
import torch.optim as optim
from numpy import ndarray
from torch.utils.data import DataLoader, Dataset

from ..utils import AverageMeter


class DictDatasetWrapper(Dataset):
    def __init__(self, data: Dict[Any, Any]):
        self.data = {
            "train_input": data["train_input"],
            "train_label": data["train_label"],
        }

        self.len = None

        for k, v in self.data.items():
            if self.len is None:
                self.len = len(v)
            elif len(v) != self.len:
                raise ValueError("Unmatched length!")

    def __len__(self):
        return self.len

    def __getitem__(self, index):
        ret = {}
        for k, v in self.data.items():
            ret[k] = v[index]
        return ret


class MLPWithTrainer(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(MLPWithTrainer, self).__init__()
        layers = []

        # 输入层
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.GELU())

        # 隐藏层
        for _ in range(num_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.GELU())

        # 输出层
        layers.append(nn.Linear(hidden_size, output_size))

        # 将层合并为一个序列
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

    def train(self, dataset: Dict[str, ndarray], *, loss_fn, lr, device, **kwargs):
        super().train()
        optimizer = torch.optim.Adam(params=self.parameters(), lr=lr)

        dataset = DictDatasetWrapper(dataset)
        dataloader = DataLoader(dataset, batch_size=256, shuffle=False)

        self.to(device)
        running_loss = AverageMeter()

        for inp in dataloader:
            optimizer.zero_grad()  # 清除梯度

            inputs = inp["train_input"]
            labels = inp["train_label"]

            # 正向传播
            outputs = self.forward(inputs)
            loss = loss_fn(outputs, labels)

            # 反向传播和优化
            loss.backward()
            optimizer.step()

            running_loss.update(loss.detach().cpu().numpy())

        return running_loss.avg
