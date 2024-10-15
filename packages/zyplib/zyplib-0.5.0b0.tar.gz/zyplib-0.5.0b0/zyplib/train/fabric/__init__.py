from typing import Optional

from lightning.fabric import Fabric, loggers

from zyplib.utils.time import now

from .basic_trainer import BasicFabricTrainer
from .callbacks import PrintTrainInfo, SaveCheckpoints, SaveHparams

__all__ = ['BasicFabricTrainer', 'default_fabric']


def default_fabric(
    dir_prefix: str = 'lightning_logs',
    save_every_k: Optional[int] = None,
    save_best: bool = True,
    keep_best_k: Optional[int] = 1,
    monitor: str = 'loss',
    less_is_better: bool = True,
):
    time_str = now()
    fabric = Fabric(
        loggers=[
            loggers.CSVLogger(root_dir='./', prefix=dir_prefix, version=f'v{time_str}'),
            loggers.TensorBoardLogger(
                root_dir='./', prefix=dir_prefix, version=f'v{time_str}'
            ),
        ],
        callbacks=[
            PrintTrainInfo(),
            SaveHparams(dir=f'./{dir_prefix}/v{time_str}'),
            SaveCheckpoints(
                dir=f'./{dir_prefix}/v{time_str}/checkpoints',
                save_every_k=save_every_k,
                save_best=save_best,
                keep_best_k=keep_best_k,
                monitor=monitor,
                less_is_better=less_is_better,
            ),
        ],
    )
    return fabric
