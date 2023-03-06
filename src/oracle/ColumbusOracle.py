from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import pandas as pd

from src.oracle import (
    HashMap,
    get_coverage_from_nodes,
    get_interestingness_from_nodes,
    get_specificity_from_nodes,
    get_uniqueness_from_nodes,
)

if TYPE_CHECKING:
    from ..space.Node import VisualizationNode


@dataclass
class OracleWeight:
    coverage: float = 1.0
    uniqueness: float = 1.0
    specificity: float = 1.0
    interestingness: float = 1.0

    def to_dict(self) -> dict[str, float]:
        return {
            "coverage": self.coverage,
            "uniqueness": self.uniqueness,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
        }


@dataclass
class OracleResult:
    weight: OracleWeight
    coverage: float
    uniqueness: float
    specificity: float
    interestingness: float

    def get_score(self) -> float:
        return (
            self.weight.coverage * self.coverage
            + self.weight.uniqueness * self.uniqueness
            + self.weight.interestingness * self.interestingness
            + self.weight.specificity * self.specificity
        )

    def __str__(self) -> str:
        return f"""
Coverage: {self.coverage}
Uniqueness: {self.uniqueness}
Specificity: {self.specificity}
Interestingness: {self.interestingness}
        """

    def to_dict(self) -> dict[str, float]:
        return {
            "coverage": self.coverage,
            "uniqueness": self.uniqueness,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
        }


@dataclass
class ColumbusOracle:
    weight: OracleWeight

    def get_result(
        self,
        nodes: list["VisualizationNode"],
        df: pd.DataFrame,
        wildcard: set[str],
        hashmap: HashMap,
    ) -> OracleResult:
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, df),
            uniqueness=get_uniqueness_from_nodes(nodes),
            interestingness=get_interestingness_from_nodes(nodes, hashmap),
            specificity=get_specificity_from_nodes(nodes, wildcard),
        )
