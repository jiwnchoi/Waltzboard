from typing import TYPE_CHECKING
from dataclasses import dataclass

import pandas as pd

from gleaner.oracle import OracleResult, OracleWeight
from gleaner.oracle.scores import (
    get_coverage_from_nodes,
    get_diversity_from_nodes,
    get_interestingness,
    get_specificity_from_nodes,
    get_conciseness_from_nodes,
    get_statistic_features,
)

if TYPE_CHECKING:
    from gleaner.model import GleanerDashboard, GleanerChart


class Oracle:
    df: pd.DataFrame

    def __init__(self, df) -> None:
        self.df = df
        self.weight = OracleWeight()

    def get_result(self, dashboard: "GleanerDashboard", preferences: set[str]) -> OracleResult:
        nodes = dashboard.charts
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, self.df),
            diversity=get_diversity_from_nodes(nodes, preferences),
            interestingness=get_interestingness(nodes),
            specificity=get_specificity_from_nodes(nodes, preferences),
            conciseness=get_conciseness_from_nodes(nodes, self.df),
        )

    def get_statistics_from_chart(self, chart: "GleanerChart") -> dict[str, list[str | None]]:
        return get_statistic_features(chart)

    def update(
        self,
        specificity: float | None = None,
        interestingness: float | None = None,
        coverage: float | None = None,
        diversity: float | None = None,
        conciseness: float | None = None,
    ) -> None:
        if specificity is not None:
            self.weight.specificity = specificity
        if interestingness is not None:
            self.weight.interestingness = interestingness
        if coverage is not None:
            self.weight.coverage = coverage
        if diversity is not None:
            self.weight.diversity = diversity
        if conciseness is not None:
            self.weight.conciseness = conciseness
