import operator
from pathlib import Path
from typing import Any, Dict, Optional, Protocol

import simple_inject as sij

from zyplib.nn.utils import save_checkpoint
from zyplib.utils.fs import ensure_dir, write_yaml
from zyplib.utils.print import print_debug, print_info
from zyplib.utils.time import TicToc, now


class FabricCallbackProtocal(Protocol):
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


class SaveHparams(FabricCallbackProtocal):
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
        """
        self.path = Path(dir) / 'hparams.yaml'
        self.inject_namespace = inject_namespace

    def on_train_start(self, **kwargs):
        hparams = kwargs['hparams']
        if hparams is None:
            hparams = sij.state(self.inject_namespace)
        if hparams:
            write_yaml(self.path, hparams)


class PrintTrainInfo(FabricCallbackProtocal):
    def __init__(self):
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


class SaveCheckpoints(FabricCallbackProtocal):
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
