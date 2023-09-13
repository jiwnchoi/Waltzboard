from typing import TYPE_CHECKING
from dataclasses import dataclass

import pandas as pd
from gleaner.oracle import OracleResult, OracleSingleResult
from gleaner.oracle.scores import *

if TYPE_CHECKING:
    from gleaner.model import GleanerDashboard, BaseChart
    from gleaner.config import GleanerConfig


class Oracle:
    df: pd.DataFrame

    def __init__(self, config: "GleanerConfig") -> None:
        self.df = config.df
        self.weight = config.weight
        self.config = config

    def get_single_chart_results(
        self, dashboard: "GleanerDashboard", target: int, preferences: set[str]
    ) -> OracleResult:
        nodes = dashboard.charts
        return OracleSingleResult(
            weight=self.weight,
            specificity=get_specificity([nodes[target]], preferences),
            interestingness=get_interestingness([nodes[target]]),
            coverage=get_coverage([nodes[target]], self.config.attr_names),
            diversity=get_diversity_single(nodes, preferences, target),
        )

    def get_result(
        self, dashboard: "GleanerDashboard", preferences: set[str]
    ) -> OracleResult:
        nodes = dashboard.charts
        return OracleResult(
            weight=self.weight,
            specificity=get_specificity(nodes, preferences),
            interestingness=get_interestingness(nodes),
            coverage=get_coverage(nodes, self.config.attr_names),
            diversity=get_diversity(nodes, preferences),
            parsimony=get_parsimony(nodes, self.config.attr_names),
        )

    def get_statistics_from_chart(self, chart: "BaseChart") -> list[Statistics]:
        return get_statistics(chart)
