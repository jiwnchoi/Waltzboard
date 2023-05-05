from dataclasses import dataclass


@dataclass
class ExplorerConfig:
    n_epoch: int = 100
    n_candidates: int  = 100
    halving_ratio: float = 0.1
    