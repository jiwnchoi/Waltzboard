from dataclasses import dataclass

import pandas as pd

from src.oracle import OracleWeight, OracleResult
from src.oracle.scores import (
    get_coverage_from_nodes,
    get_diversity_from_nodes,
    get_interestingness,
    get_specificity_from_nodes,
)

from src.model import GleanerChart, GleanerDashboard


@dataclass
class Oracle:
    df: pd.DataFrame
    weight: OracleWeight

    def get_result(
        self, dashboard: GleanerDashboard, wildcard: set[str]
    ) -> OracleResult:
        nodes = dashboard.charts
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, self.df),
            diversity=get_diversity_from_nodes(nodes),
            interestingness=get_interestingness(nodes),
            specificity=get_specificity_from_nodes(nodes, wildcard),
            conciseness=len(self.df.columns) / len(nodes),
        )
