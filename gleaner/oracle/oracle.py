from typing import TYPE_CHECKING
from dataclasses import dataclass

import pandas as pd
from gleaner.oracle import OracleResult, OracleWeight
from gleaner.oracle.scores import (
    get_coverage_from_nodes,
    get_diversity_from_nodes,
    get_interestingness,
    get_specificity_from_nodes,
    get_parsimony_from_nodes,
    get_statistic_features,
)

if TYPE_CHECKING:
    from gleaner.model import GleanerDashboard, GleanerChart
    from gleaner.config import GleanerConfig


class Oracle:
    df: pd.DataFrame

    def __init__(self, config: "GleanerConfig") -> None:
        self.df = config.df
        self.weight = config.weight
        self.config = config

    def get_result(self, dashboard: "GleanerDashboard", preferences: set[str]) -> OracleResult:
        nodes = dashboard.charts
        return OracleResult(
            weight=self.weight,
            specificity=get_specificity_from_nodes(nodes, preferences),
            interestingness=get_interestingness(nodes),
            coverage=get_coverage_from_nodes(nodes, self.df),
            diversity=get_diversity_from_nodes(nodes, preferences),
            parsimony=get_parsimony_from_nodes(nodes, self.df),
        )

    def get_statistics_from_chart(self, chart: "GleanerChart") -> dict[str, list[str | None]]:
        return get_statistic_features(chart)
