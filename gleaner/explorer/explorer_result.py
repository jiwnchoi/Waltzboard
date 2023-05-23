from dataclasses import dataclass
import numpy as np


@dataclass
class TrainResult:
    scores: np.ndarray
    specificity: np.ndarray
    interestingness: np.ndarray
    coverage: np.ndarray
    diversity: np.ndarray
    parsimony: np.ndarray
    n_charts: np.ndarray
