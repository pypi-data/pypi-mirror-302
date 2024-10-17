import csv
import operator
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Optional, Protocol

import openpyxl
import simple_inject as sij
from lightning import Fabric

from zyplib.nn.utils import save_checkpoint
from zyplib.train.utils import prefixed_dict
from zyplib.utils.fs import ensure_dir, write_yaml
from zyplib.utils.print import print_debug, print_info, print_warn
from zyplib.utils.time import TicToc, now


class FabricCallbackProtocol(Protocol):
    def on_train_start(self, **kwargs): ...

    def on_train_end(self, **kwargs): ...

    def on_train_batch_start(self, batch: Any, batch_idx: int, **kwargs): ...

    def on_train_batch_end(self, batch: Any, batch_idx: int, **kwargs): ...

    def on_train_epoch_start(self, **kwargs): ...

    def on_train_epoch_end(self, **kwargs): ...

    def on_validation_start(self, **kwargs): ...

    def on_validation_end(self, **kwargs): ...

    def on_validation_batch_start(self, batch: Any, batch_idx: int, **kwargs): ...

    def on_validation_batch_end(self, batch: Any, batch_idx: int, **kwargs): ...

    def on_validation_epoch_start(self, **kwargs): ...

    def on_validation_epoch_end(self, **kwargs): ...

    def on_test_start(self, **kwargs): ...

    def on_test_end(self, **kwargs): ...

    def on_test_batch_start(self, batch: Any, batch_idx: int, **kwargs): ...

    def on_test_batch_end(self, batch: Any, batch_idx: int, **kwargs): ...

    def on_exception(self, exception: BaseException, **kwargs): ...

    def on_fit_start(self, **kwargs): ...

    def on_fit_end(self, **kwargs): ...


class EnsureFabricMixin:
    def __init__(self, fabric: Optional[Fabric] = None):
        self.fabric = fabric

    def on_train_start(self, **kwargs):
        if self.fabric is not None:
            return
        fabric = kwargs.get('fabric', None)
        if fabric is None:
            classname = self.__class__.__name__
            raise ValueError(f'{classname} 必须有一个 fabric 属性!')
        self.fabric = fabric


class SaveHparams(FabricCallbackProtocol):
    def __init__(self, dir: str, inject_namespace: str = 'default'):
        """自动保存超参数

        将超参数保存到 `dir`/hparams.yaml 下

        `on_train_start`
        ----------
        - 可以将 `hparams` 作为参数传入
        - 如果未传入，则从 `simple_inject` 中获取 namespace 的字典

        Parameters
        ----------
        - `dir` : `str`
            - 保存目录
        - `inject_namespace` : `str`
            - 从 `simple_inject` 中获取超参数的字典

        Hooks
        -----
        - `on_train_start`
            - `hparams` : `Dict[str, Any]`: 超参数; 如果未传入，则从 `simple_inject` 中获取
        """
        self.path = Path(dir) / 'hparams.yaml'
        self.inject_namespace = inject_namespace

    def on_train_start(self, **kwargs):
        hparams = kwargs['hparams']
        if hparams is None:
            hparams = sij.state(self.inject_namespace)
        if hparams:
            write_yaml(self.path, hparams)


class PrintTrainInfo(FabricCallbackProtocol):
    def __init__(self):
        """打印训练信息

        打印训练信息到控制台

        Hooks
        -----
        - `on_train_start`: 打印训练开始信息, 记录训练开始时间
        - `on_train_end`: 打印训练结束信息, 记录训练结束时间
        - `on_train_epoch_start`: 打印当前 epoch 信息
            - `epoch` : `int`: 当前 epoch 数
            - `max_epochs` : `int`: 最大 epoch 数
        - `on_train_epoch_end`: 打印当前 epoch 训练指标
            - `metrics` : `Dict[str, float]`: 当前 epoch 的训练指标
        - `on_validation_epoch_end`: 打印当前 epoch 验证指标
            - `metrics` : `Dict[str, float]`: 当前 epoch 的验证指标
        - `on_test_end`: 打印测试指标
            - `metrics` : `Dict[str, float]`: 测试指标
        """
        self.tictoc = TicToc()

    def _print_epoch_summary(self, metrics: Dict[str, float]):
        for key, value in metrics.items():
            print_info(f'\t{key}: {value:.4f}', end='')
        print()

    def on_train_start(self, **kwargs):
        self.tictoc.tic()
        print_info(f'开始训练: {now()}'.center(80, '='))
        print()

    def on_train_end(self, **kwargs):
        self.tictoc.toc()
        print()
        self.tictoc.print_elapsed('This training')
        print_info(f'结束训练: {now()}'.center(80, '='))

    def on_train_epoch_start(self, epoch: int, max_epochs: int, **kwargs):
        print_info(f'Epoch {epoch}/{max_epochs}'.center(50, '-'))

    def on_train_epoch_end(self, metrics: Dict[str, float], **kwargs):
        print_info('Train |', end='')
        self._print_epoch_summary(metrics)

    def on_validation_epoch_end(self, metrics: Dict[str, float], **kwargs):
        print_info('Val | ', end='')
        self._print_epoch_summary(metrics)

    def on_test_end(self, metrics: Dict[str, float], **kwargs):
        print_info('Test | ', end='')
        self._print_epoch_summary(metrics)


class SaveCheckpoints(FabricCallbackProtocol):
    def __init__(
        self,
        dir: str,
        save_every_k: Optional[int] = None,
        save_best: bool = True,
        keep_best_k: Optional[int] = 1,
        monitor: str = 'loss',
        less_is_better: bool = True,
        ckpt_ext: str = '.ckpt',
    ):
        """自动保存模型检查点

        Parameters
        ----------
        - `dir` : `str`
            - 保存检查点的目录
        - `save_every_k` : `Optional[int]`, optional
            - 每多少个epoch保存一次，默认为None
        - `save_best` : `bool`, optional
            - 是否保存最佳模型，默认为True
        - `keep_best_k` : `Optional[int]`, optional
            - 只保存最佳模型的数量，默认为 1;
        - `monitor` : `str`, optional
            - 用于确定最佳模型的指标，默认为'loss'
            - 可以有 `train_` 和 `val_` 前缀
            - 如果没有前缀，则优先使用 val_metrics
        - `less_is_better` : `bool`, optional
            - 是否为越小越优，默认为True
        - `ckpt_ext` : `str`, optional
            - 检查点文件的扩展名，默认为'.ckpt'

        Hooks
        -----
        - `on_train_start`
            - `model` : `nn.Module`: 模型
            - `optimizer` : `Optimizer`: 优化器
            - `lr_scheduler` : `_LRScheduler`: 学习率调度器
        - `on_train_epoch_start`: 清空内置的 train 和 val 指标缓存
        - `on_train_epoch_end`
            - `metrics` : `Dict[str, float]`: 更新当前 epoch 的训练指标
        - `on_validation_epoch_end`
            - `metrics` : `Dict[str, float]`: 更新当前 epoch 的验证指标
        - `on_epoch_end`: 保存检查点
        """

        ensure_dir(dir)

        self.dir = Path(dir)
        self.save_every_k = save_every_k
        self.save_best = save_best
        self.keep_best_k = keep_best_k
        self.monitor = monitor
        self.best_score = float('inf') if less_is_better else float('-inf')
        self.current_epoch = 0

        self.score_cmp = operator.lt if less_is_better else operator.gt
        self.ckpt_ext = ckpt_ext

    def on_train_start(self, *, model, optimizer, lr_scheduler, **kwargs):
        self.model = model
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def on_train_epoch_start(self, **kwargs):
        self.train_metrics = None
        self.val_metrics = None

    def on_train_epoch_end(self, metrics: dict, **kwargs):
        self.train_metrics = metrics

    def on_validation_epoch_end(self, metrics: dict, **kwargs):
        self.val_metrics = metrics

    def on_epoch_end(self, **kwargs):
        self.current_epoch += 1

        # 定期保存检查点
        if self.save_every_k and self.current_epoch % self.save_every_k == 0:
            checkpoint_path = (
                self.dir / f'checkpoint_epoch={self.current_epoch}{self.ckpt_ext}'
            )
            self._save(checkpoint_path)
            print_debug(f'Saved checkpoint at epoch {self.current_epoch}')

        if not self.save_best:
            return

        metrics = self.val_metrics or self.train_metrics
        if not metrics:
            return

        current_score = (
            metrics.get(self.monitor)
            or metrics.get(f'val_{self.monitor}')
            or metrics.get(f'train_{self.monitor}')
        )

        if current_score is None:
            return

        if not self.score_cmp(current_score, self.best_score):
            return

        self.best_score = current_score
        best_model_name = self.__format_best_model_fname(
            epoch=self.current_epoch, monitor=self.monitor, score=current_score
        )
        checkpoint_path = self.dir / best_model_name
        self._save(checkpoint_path)
        print_debug(
            f'Saved best model at epoch {self.current_epoch} with {self.monitor}: {current_score:.4f}'
        )

        # 保留最佳 K 个模型
        if self.keep_best_k:
            checkpoints = sorted(
                self.dir.glob(f'best_model_*{self.ckpt_ext}'),
                key=lambda x: self.__extract_best_model_info(x.name)['score'],
                reverse=not self.score_cmp(0, 1),  # True if higher is better
            )
            if len(checkpoints) > self.keep_best_k:
                for checkpoint in checkpoints[self.keep_best_k :]:
                    checkpoint.unlink()

    def __format_best_model_fname(
        self,
        epoch: Optional[int] = None,
        monitor: Optional[str] = None,
        score: Optional[float] = None,
    ):
        epoch_part = f'_epoch={epoch}' if epoch else ''
        monitor_part = f'_on={monitor}' if monitor else ''
        score_part = f'_score={score:.4f}' if score else ''

        return f'best_model{epoch_part}{monitor_part}{score_part}{self.ckpt_ext}'

    def __extract_best_model_info(self, fname: str):
        fname = fname.removesuffix(self.ckpt_ext)
        each_parts = fname.split('_')
        info = {'epoch': None, 'monitor': None, 'score': None}
        for each_part in each_parts:
            if each_part.startswith('epoch='):
                info['epoch'] = int(each_part.split('=')[-1])
            elif each_part.startswith('on='):
                info['monitor'] = each_part.split('=')[-1]
            elif each_part.startswith('score='):
                info['score'] = float(each_part.split('=')[-1])
        return info

    def _save(self, checkpoint_path: str, **kwargs):
        save_checkpoint(
            models=self.model,
            path=checkpoint_path,
            optimizers=self.optimizer,
            epoch=self.current_epoch,
            train_metrics=self.train_metrics,
            val_metrics=self.val_metrics,
            **kwargs,
        )

    @staticmethod
    def best_checkpoint(dir: str, ext: str = '.ckpt') -> Path:
        return sorted(
            Path(dir).glob(f'best_model*{ext}'),
            key=lambda x: x.name.removesuffix(ext).split('=')[-1],
            reverse=True,
        )[0]


class MonitorLearningRate(EnsureFabricMixin, FabricCallbackProtocol):
    def __init__(self, fabric: Optional[Fabric] = None):
        """监控学习率

        监控学习率的变化，并记录到 fabric 的 loggers 中

        Parameters
        ----------
        - `fabric` : `Fabric`
            - 训练使用的 fabric 对象

        Hooks
        -----
        - `on_train_start`
            - `optimizer` : `Optimizer`: 优化器
            - `lr_scheduler` : `_LRScheduler`: 学习率调度器
        - `on_train_epoch_start`
            - `epoch` : `int`: 当前 epoch 数
        """
        EnsureFabricMixin.__init__(self, fabric)

    def on_train_start(self, *, optimizer, lr_scheduler, **kwargs):
        EnsureFabricMixin.on_train_start(self, **kwargs)
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

    def on_train_epoch_start(self, **kwargs):
        self.lr = self.optimizer.param_groups[0]['lr']
        epoch = kwargs.get('epoch', None)
        self.fabric.log('learning_rate', self.lr, epoch)


class FabricLogMetrics(EnsureFabricMixin, FabricCallbackProtocol):
    def __init__(self, fabric: Optional[Fabric] = None):
        """使用 Fabric 记录训练过程中的指标 (`fabric.log_dict`)

        Parameters
        ----------
        - `fabric` : `Fabric`, optional
            - 用于记录指标的 fabric 实例，默认为 None
            - 如果未传入，则会在 `on_train_start` 中从 kwargs 中获取 `fabric` 对象
            - *如果仍然为 None，则会抛出 ValueError

        Hooks
        -----
        - `on_train_start`
            - `fabric` : 可选的 `Fabric`
        - `on_train_batch_end`
            - `metrics` : `Dict[str, Any]`
        - `on_validation_batch_end`
            - `metrics` : `Dict[str, Any]`
        - `on_train_epoch_end`
            - `metrics` : `Dict[str, Any]`
            - `epoch` : `int`
        - `on_validation_epoch_end`
            - `metrics` : `Dict[str, Any]`
            - `epoch` : `int`
        - `on_test_end`
            - `metrics` : `Dict[str, Any]`
        """
        EnsureFabricMixin.__init__(self, fabric)
        self.train_batch_idx = 0
        self.val_batch_idx = 0

    def on_train_batch_end(self, metrics: Dict[str, Any], *args, step: Optional[int] = None, **kwargs):
        metrics = prefixed_dict('train_', metrics)
        if step is None:
            step = self.train_batch_idx
            self.train_batch_idx += 1
        else:
            self.train_batch_idx = step
        self.fabric.log_dict(metrics, step=step)

    def on_validation_batch_end(self, metrics: Dict[str, Any], *args, step: Optional[int] = None, **kwargs):
        metrics = prefixed_dict('val_', metrics)
        if step is None:
            step = self.val_batch_idx
            self.val_batch_idx += 1
        else:
            self.val_batch_idx = step
        self.fabric.log_dict(metrics, step=step)

    def on_train_epoch_end(self, metrics: Dict[str, Any], epoch: int, **kwargs):
        metrics = prefixed_dict('train_epoch_', metrics)
        self.fabric.log_dict(metrics, step=epoch)

    def on_validation_epoch_end(self, metrics: Dict[str, Any], epoch: int, **kwargs):
        metrics = prefixed_dict('val_epoch_', metrics)
        self.fabric.log_dict(metrics, step=epoch)

    def on_test_end(self, metrics: Dict[str, Any], epoch: Optional[int] = None, **kwargs):
        metrics = prefixed_dict('test_', metrics)
        self.fabric.log_dict(metrics, step=epoch)


class ParseCSVLogfile:
    def __init__(self, csv_fpath: str, to_excel: bool = True, to_yaml: bool = True):
        self.csv_fpath = Path(csv_fpath)
        self.to_excel = to_excel
        self.to_yaml = to_yaml
        self.excel_fpath = self.csv_fpath.parent / f'{self.csv_fpath.name}.xlsx'
        self.yaml_fpath = self.csv_fpath.parent / f'{self.csv_fpath.name}.yaml'

        if not (to_excel or to_yaml):
            raise ValueError("At least one of 'to_excel' or 'to_yaml' must be True")

    def _process_csv(self):
        # Read CSV file
        with open(self.csv_fpath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

        # Process and organize data
        organized_data = defaultdict(lambda: defaultdict(list))
        metrics = set()

        for row in data:
            step = int(row.get('step', 0))
            for key, value in row.items():
                if key not in ['step'] and value:
                    metrics.add(key)
                    organized_data[key][step].append(float(value))

        # 不知道为啥 logger 会重复记录，所以这里简单取平均
        repeated_metrics = set()
        for metric in organized_data:
            for step in organized_data[metric]:
                if len(organized_data[metric][step]) > 1:
                    repeated_metrics.add(metric)
                organized_data[metric][step] = sum(organized_data[metric][step]) / len(
                    organized_data[metric][step]
                )
        if repeated_metrics:
            print_warn(f'发现 CSV Logger 存在重复记录的指标: {repeated_metrics}')

        return organized_data, metrics

    def _to_yaml(self, organized_data, metrics):
        names = sorted(list(metrics))
        final_data = {name: dict(organized_data[name]) for name in names}
        write_yaml(self.yaml_fpath, final_data)

    def _to_excel(self, organized_data, metrics):
        wb = openpyxl.Workbook()

        # Create sheets for each metric
        for metric in metrics:
            sheet = wb.create_sheet(title=metric)
            sheet['A1'] = 'Step'
            sheet['B1'] = 'Value'
            row = 2
            for step, value in sorted(organized_data[metric].items()):
                sheet[f'A{row}'] = step
                sheet[f'B{row}'] = value
                row += 1

        # Remove the default sheet created by openpyxl
        wb.remove(wb['Sheet'])

        # Save the Excel file
        wb.save(self.excel_fpath)

    def _convert(self):
        if not self.to_excel and not self.to_yaml:
            return
        if not self.csv_fpath.exists():
            print_warn(f'CSV 日志文件不存在, 无法转换: {self.csv_fpath}')
            return
        organized_data, metrics = self._process_csv()
        if self.to_yaml:
            self._to_yaml(organized_data, metrics)
        if self.to_excel:
            self._to_excel(organized_data, metrics)

    def on_train_end(self, **kwargs):
        self._convert()

    def on_validation_end(self, **kwargs):
        self._convert()

    def on_test_end(self, **kwargs):
        self._convert()
