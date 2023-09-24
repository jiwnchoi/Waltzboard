from typing import TYPE_CHECKING
from dataclasses import dataclass

import pandas as pd
from waltzboard.oracle import OracleResult, OracleSingleResult
from waltzboard.oracle.scores import *

if TYPE_CHECKING:
    from waltzboard.model import WaltzboardDashboard, BaseChart
    from waltzboard.config import WaltzboardConfig


class Oracle:
    df: pd.DataFrame

    def __init__(self, config: "WaltzboardConfig") -> None:
        self.df = config.df
        self.weight = config.weight
        self.config = config

    def get_single_chart_results(
        self, dashboard: "WaltzboardDashboard", target: int, preferences: set[str]
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
        self, dashboard: "WaltzboardDashboard", preferences: set[str]
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
