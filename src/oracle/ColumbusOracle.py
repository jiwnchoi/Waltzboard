from src.oracle import OracleWeight, OracleResult
from src.oracle import (
    get_coverage_from_nodes,
    get_uniqueness_from_nodes,
    get_interestingness_from_nodes,
    get_specificity_from_nodes,
)
from typing import TYPE_CHECKING, Optional
import pandas as pd

if TYPE_CHECKING:
    from ..space.Node import VisualizationNode


class ColumbusOracle:
    def __init__(self, weight: Optional[OracleWeight]) -> None:
        self.weight = OracleWeight() if weight is None else weight

    def get_result(
        self, nodes: list["VisualizationNode"], df: pd.DataFrame, wildcard: set[str]
    ) -> OracleResult:
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, df),
            uniqueness=get_uniqueness_from_nodes(nodes),
            interestingness=get_interestingness_from_nodes(nodes, df),
            specificity=get_specificity_from_nodes(nodes, wildcard),
        )
