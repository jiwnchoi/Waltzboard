from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

from .oracle_weight import OracleWeight

if TYPE_CHECKING:
    from waltzboard.oracle import Normalizer


@dataclass
class OracleResult:
    weight: OracleWeight
    coverage: float
    diversity: float
    specificity: float
    interestingness: float
    parsimony: float

    def get_score(self) -> float:
        return (
            self.weight.coverage * self.coverage
            + self.weight.diversity * self.diversity
            + self.weight.interestingness * self.interestingness
            + self.weight.specificity * self.specificity
            + self.weight.parsimony * self.parsimony
        )

    def get_normalized_score(self, normalizer: "Normalizer") -> float:
        return (
            self.weight.coverage * normalizer.normalize_one(self.coverage, "coverage")
            + self.weight.diversity
            * normalizer.normalize_one(self.diversity, "diversity")
            + self.weight.interestingness
            * normalizer.normalize_one(self.interestingness, "interestingness")
            + self.weight.specificity
            * normalizer.normalize_one(self.specificity, "specificity")
            + self.weight.parsimony
            * normalizer.normalize_one(self.parsimony, "parsimony")
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "score": self.get_score(),
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "parsimony": self.parsimony,
        }

    def display(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.to_dict(), orient="index", columns=["value"])
