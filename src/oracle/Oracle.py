from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

from . import OracleWeight, OracleResult
from .scores import (
    get_coverage_from_nodes,
    get_diversity_from_nodes,
    get_interestingness,
    get_specificity_from_nodes,
)

if TYPE_CHECKING:
    from ..model.Node import VisualizationNode


@dataclass
class Oracle:
    df: pd.DataFrame
    weight: OracleWeight

    def get_result(
        self, nodes: list["VisualizationNode"], wildcard: set[str]
    ) -> OracleResult:
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, self.df),
            diversity=get_diversity_from_nodes(nodes),
            interestingness=get_interestingness(nodes),
            specificity=get_specificity_from_nodes(nodes, wildcard),
            conciseness=len(self.df.columns) / len(nodes),
        )
