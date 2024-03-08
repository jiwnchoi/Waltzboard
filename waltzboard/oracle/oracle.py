from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from .oracle_result import OracleResult
from .scores import (
    Statistics,
    get_coverage,
    get_diversity,
    get_interestingness,
    get_parsimony,
    get_specificity,
    get_statistics,
)

if TYPE_CHECKING:
    from waltzboard.config import WaltzboardConfig
    from waltzboard.model import BaseChart, WaltzboardDashboard


class Oracle:
    df: pd.DataFrame

    def __init__(self, config: "WaltzboardConfig") -> None:
        self.df = config.df
        self.weight = config.weight
        self.config = config

    def get_result(
        self, dashboard: "WaltzboardDashboard", preferences: set[str]
    ) -> OracleResult:
        nodes = dashboard.charts
        return OracleResult(
            weight=self.weight,
            specificity=get_specificity(nodes, preferences),
            interestingness=get_interestingness(nodes),
            coverage=get_coverage(nodes, self.config.raw_attr_names),
            diversity=get_diversity(nodes, preferences),
            parsimony=get_parsimony(nodes, self.config),
        )

    def get_statistics_from_chart(self, chart: "BaseChart") -> list[Statistics]:
        return get_statistics(chart)


@dataclass
class Normalizer:
    means = {
        "specificity": "specificity_mean",
        "interestingness": "interestingness_mean",
        "coverage": "coverage_mean",
        "diversity": "diversity_mean",
        "parsimony": "parsimony_mean",
    }
    stds = {
        "specificity": "specificity_std",
        "interestingness": "interestingness_std",
        "coverage": "coverage_std",
        "diversity": "diversity_std",
        "parsimony": "parsimony_std",
    }

    specificity_mean: float
    specificity_std: float
    interestingness_mean: float
    interestingness_std: float
    coverage_mean: float
    coverage_std: float
    diversity_mean: float
    diversity_std: float
    parsimony_mean: float
    parsimony_std: float
    on: bool = False

    def normalize(self, scores: np.ndarray, score_type: str):
        if not self.on:
            return scores
        if self.stds[score_type] == 0:
            return scores
        s = (scores - getattr(self, self.means[score_type])) / getattr(
            self, self.stds[score_type]
        )
        return s

    def normalize_one(self, score: float, score_type: str):
        if not self.on:
            return score
        if self.stds[score_type] == 0:
            return score
        s = (score - getattr(self, self.means[score_type])) / getattr(
            self, self.stds[score_type]
        )
        return s
