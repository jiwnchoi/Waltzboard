from dataclasses import dataclass

import numpy as np


@dataclass
class TrainResult:
    score: np.ndarray
    specificity: np.ndarray
    interestingness: np.ndarray
    coverage: np.ndarray
    diversity: np.ndarray
    parsimony: np.ndarray
    n_charts: np.ndarray

    def to_dict(self):
        return {
            "score": self.score.tolist(),
            "specificity": self.specificity.tolist(),
            "interestingness": self.interestingness.tolist(),
            "coverage": self.coverage.tolist(),
            "diversity": self.diversity.tolist(),
            "parsimony": self.parsimony.tolist(),
        }
