import os
from typing import Callable, Optional

from lightning.fabric import Fabric, loggers

from zyplib.utils.time import now

from .basic_trainer import BasicFabricTrainer
from .callbacks import (
    FabricCallbackProtocol,
    ParseCSVLogfile,
    PrintTrainInfo,
    SaveCheckpoints,
    SaveHparams,
)

__all__ = ['BasicFabricTrainer', 'default_fabric']


def default_fabric(
    dir_name: str = 'lightning_logs',
    save_every_k: Optional[int] = None,
    save_best: bool = True,
    keep_best_k: Optional[int] = 1,
    monitor: str = 'loss',
    less_is_better: bool = True,
    no_csv_logger: bool = False,
    no_tensorboard_logger: bool = False,
    no_print_info_cb: bool = False,
    no_save_checkpoints_cb: bool = False,
    no_save_hparams_cb: bool = False,
    fn_custom_logger: Optional[Callable[[str], list[loggers.Logger]]] = None,
    fn_custom_callback: Optional[Callable[[str], list[FabricCallbackProtocol]]] = None,
    **fabric_kwargs,
):
    """构建默认的fabric对象

    默认配置下，会将 logger 和 checkpoint 保存在 `dir_name/v{time_str}` 目录下; 例如 `lightning_logs/v2024-05-01 12:00:00`

    默认配置如下:
    - Loggers:
        - CSVLogger
        - TensorBoardLogger
    - Callbacks:
        - PrintTrainInfo
        - SaveHparams
        - SaveCheckpoints

    可以通过 `fn_custom_xxx` 参数来添加自定义的 logger 和 callback; 该回调函数传入 now 的时间字符串，需要返回一个 logger 或者 callback 的列表

    Parameters
    ----------
    - `dir_name` : `str`, optional
        - 日志保存的目录, by default 'lightning_logs'
    - `save_every_k` : `Optional[int]`, SaveCheckpoints 的参数
        - 每多少个epoch保存一次模型, by default None
    - `save_best` : `bool`, SaveCheckpoints 的参数
        - _description_, by default True
    - `keep_best_k` : `Optional[int]`, SaveCheckpoints 的参数
        - 保存最好的k个模型, by default 1
    - `monitor` : `str`, SaveCheckpoints 的参数
        - 监控的指标, by default 'loss'
    - `less_is_better` : `bool`, SaveCheckpoints 的参数
        - 是否监控指标越小越好, by default True
    - `no_csv_logger` : `bool`, optional
        - 是否禁用CSVLogger, by default False
    - `no_tensorboard_logger` : `bool`, optional
        - 是否禁用TensorBoardLogger, by default False
    - `no_print_info_cb` : `bool`, optional
        - 是否禁用打印训练信息回调, by default False
    - `no_save_checkpoints_cb` : `bool`, optional
        - 是否禁用保存检查点回调, by default False
    - `no_save_hparams_cb` : `bool`, optional
        - 是否禁用保存超参数回调, by default False
    - `fn_custom_logger` : `(now: string) => Logger[]`, optional
        - 自定义 logger 的函数, by default None
    - `fn_custom_callback`: `(now: string) => FabricCallbackProtocol[]`
        - 自定义 callback 的函数, by default None

    Returns
    ----------
    - `fabric` : `Fabric`
        - Fabric 对象; 注意只返回 fabric，不自动调用 fabric.launch()
    """
    time_str = now()
    _loggers = []
    _callbacks = []

    # Add loggers if not disabled
    if not no_csv_logger:
        csv = loggers.CSVLogger(root_dir='./', name=dir_name, version=f'v{time_str}')
        _loggers.append(csv)
        parser = ParseCSVLogfile(os.path.join(csv.log_dir, 'metrics.csv'))
        _callbacks.append(parser)
    if not no_tensorboard_logger:
        _loggers.append(
            loggers.TensorBoardLogger(
                root_dir='./', name=dir_name, version=f'v{time_str}'
            )
        )

    if fn_custom_logger:
        custom_loggers = fn_custom_logger(time_str)
        if isinstance(custom_loggers, list):
            _loggers.extend(custom_loggers)
        else:
            raise ValueError(
                f'fn_custom_logger must return a list of loggers, but got {type(custom_loggers)}'
            )

    # Add callbacks if not disabled
    if not no_print_info_cb:
        _callbacks.append(PrintTrainInfo())
    if not no_save_hparams_cb:
        _callbacks.append(SaveHparams(dir=f'./{dir_name}/v{time_str}'))
    if not no_save_checkpoints_cb:
        _callbacks.append(
            SaveCheckpoints(
                dir=f'./{dir_name}/v{time_str}/checkpoints',
                save_every_k=save_every_k,
                save_best=save_best,
                keep_best_k=keep_best_k,
                monitor=monitor,
                less_is_better=less_is_better,
            )
        )
    if fn_custom_callback:
        custom_callbacks = fn_custom_callback(time_str)
        if isinstance(custom_callbacks, list):
            _callbacks.extend(custom_callbacks)
        else:
            raise ValueError(
                f'fn_custom_callback must return a list of callbacks, but got {type(custom_callbacks)}'
            )

    fabric = Fabric(loggers=_loggers, callbacks=_callbacks, **fabric_kwargs)
    return fabric
