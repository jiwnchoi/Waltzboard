from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

from src.oracle import (
    get_coverage_from_nodes,
    get_diversity_from_nodes,
    get_interestingness_v2,
    get_specificity_from_nodes,
)

if TYPE_CHECKING:
    from ..space.Node import VisualizationNode


@dataclass
class OracleWeight:
    coverage: float = 1.0
    diversity: float = 1.0
    specificity: float = 1.0
    interestingness: float = 1.0
    conciseness: float = 1.0

    def to_dict(self) -> dict[str, float]:
        return {
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "conciseness": self.conciseness,
        }


@dataclass
class OracleResult:
    weight: OracleWeight
    coverage: float
    diversity: float
    specificity: float
    interestingness: float
    conciseness: float

    def get_score(self) -> float:
        return (
            self.weight.coverage * self.coverage
            + self.weight.diversity * self.diversity
            + self.weight.interestingness * self.interestingness
            + self.weight.specificity * self.specificity
            + self.weight.conciseness * self.conciseness
        )

    def __str__(self) -> str:
        return f"""
Score: {self.get_score()}
Coverage: {self.coverage}
diversity: {self.diversity}
Specificity: {self.specificity}
Interestingness: {self.interestingness}
Conciseness: {self.conciseness}
        """

    def to_dict(self) -> dict[str, float]:
        return {
            "score": self.get_score(),
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "conciseness": self.conciseness,
        }


@dataclass
class ColumbusOracle:
    df: pd.DataFrame
    weight: OracleWeight

    def get_result(
        self, nodes: list["VisualizationNode"], wildcard: set[str]
    ) -> OracleResult:
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, self.df),
            diversity=get_diversity_from_nodes(nodes),
            interestingness=get_interestingness_v2(nodes),
            specificity=get_specificity_from_nodes(nodes, wildcard),
            conciseness=len(self.df.columns) / len(nodes),
        )
