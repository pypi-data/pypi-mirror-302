from typing import Any, Callable, Dict, List, Literal, Optional, Union

import torch
from lightning.fabric import Fabric
from torch import nn
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import DataLoader
from torchmetrics import Metric, MetricCollection

from zyplib.train.record.torch_metric import TorchMetricRecorder
from zyplib.train.utils import prefixed_dict, step_lr_sched
from zyplib.utils.print import print_info
from zyplib.utils.progress_bar import rich_progress


class BasicFabricTrainer:
    def __init__(
        self,
        fabric: Fabric,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        fn_loss: nn.Module = None,
        hparams: Optional[Dict[str, Any]] = None,
        metrics: Optional[Union[MetricCollection, Dict[str, Metric]]] = None,
        before_metric: Optional[
            Union[Literal['sigmoid', 'softmax'], Callable, nn.Module]
        ] = None,
        lr_scheduler: Optional[_LRScheduler] = None,
        lr_sched_freq: int = 1,
        lr_sched_interval: str = 'epoch',
    ):
        self.fabric = fabric
        self.fabric.launch()

        self.hparams = hparams

        self.train_metric = TorchMetricRecorder(metrics, before_metric=before_metric)
        self.val_metric = TorchMetricRecorder(metrics, before_metric=before_metric)

        self.model = model
        self.optimizer = optimizer
        self.fn_loss = fn_loss or nn.BCEWithLogitsLoss()
        self.lr_scheduler = lr_scheduler
        self.lr_sched_freq = lr_sched_freq
        self.lr_sched_interval = lr_sched_interval

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor]) -> Dict[str, Any]:
        self.model.train()
        x, y = batch

        self.optimizer.zero_grad()
        y_pred = self.model(x)
        loss = self.fn_loss(y_pred, y)
        self.fabric.backward(loss)
        self.optimizer.step()

        metrics = self.train_metric.update(y_pred, y, loss.item())
        self.fabric.log_dict(prefixed_dict('train_', metrics))
        return metrics

    def validation_step(
        self, batch: tuple[torch.Tensor, torch.Tensor], test: bool = False
    ) -> Dict[str, Any]:
        self.model.eval()
        with torch.no_grad():
            x, y = batch
            y_pred = self.model(x)
            loss = self.fn_loss(y_pred, y)

        metrics = self.val_metric.update(y_pred, y, loss.item())
        self.fabric.log_dict(prefixed_dict('val_' if not test else 'test_', metrics))
        return metrics

    def train_epoch(self, train_loader: DataLoader, epoch_idx: int) -> Dict[str, float]:
        for batch in rich_progress(train_loader, 'Training', color='green'):
            self.training_step(batch)
        metrics = self.train_metric.compute()
        self.fabric.log_dict(prefixed_dict('train_epoch_', metrics), step=epoch_idx)
        return metrics

    def val_epoch(
        self, val_loader: DataLoader, epoch_idx: int, test: bool = False
    ) -> Dict[str, float]:
        for batch in rich_progress(
            val_loader, 'Validating' if not test else 'Testing', color='blue'
        ):
            self.validation_step(batch, test)
        metrics = self.val_metric.compute()
        if not test:
            self.fabric.log_dict(prefixed_dict('val_epoch_', metrics), step=epoch_idx)
        return metrics

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: Optional[DataLoader] = None,
        max_epochs: int = 10,
    ) -> Dict[str, List[float]]:
        self.model, self.optimizer = self.fabric.setup(self.model, self.optimizer)
        train_loader = self.fabric.setup_dataloaders(train_loader)
        if val_loader:
            val_loader = self.fabric.setup_dataloaders(val_loader)

        self.fabric.call(
            'on_train_start',
            trainer=self,
            max_epochs=max_epochs,
            hparams=self.hparams,
            model=self.model,
            optimizer=self.optimizer,
            lr_scheduler=self.lr_scheduler
        )

        for epoch in range(max_epochs):
            self.fabric.call(
                'on_train_epoch_start', trainer=self, epoch=epoch, max_epochs=max_epochs
            )

            train_metrics = self.train_epoch(train_loader, epoch)

            self.fabric.call(
                'on_train_epoch_end', trainer=self, epoch=epoch, metrics=train_metrics
            )

            if val_loader:
                self.fabric.call('on_validation_epoch_start', trainer=self, epoch=epoch)

                val_metrics = self.val_epoch(val_loader, epoch)

                self.fabric.call(
                    'on_validation_epoch_end',
                    trainer=self,
                    epoch=epoch,
                    metrics=val_metrics,
                )
            else:
                val_metrics = None

            if self.lr_scheduler and self.lr_sched_interval == 'epoch':
                if (epoch + 1) % self.lr_sched_freq == 0:
                    loss = train_metrics['loss']
                    if val_metrics:
                        loss = val_metrics['loss']
                    step_lr_sched(self.lr_scheduler, loss)

            self.fabric.call(
                'on_epoch_end',
                trainer=self,
                epoch=epoch,
                train_metrics=train_metrics,
                val_metrics=val_metrics,
            )

        self.fabric.call('on_train_end')

    def test(self, test_loader: DataLoader) -> Dict[str, float]:
        test_loader = self.fabric.setup_dataloaders(test_loader)
        result = self.val_epoch(test_loader, 0, test=True)
        self.fabric.log_dict(prefixed_dict('test_', result))
        self.fabric.call('on_test_end', trainer=self, metrics=result)
        return result
