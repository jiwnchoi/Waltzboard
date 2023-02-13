from src.oracle import OracleWeight, OracleResult
from src.oracle import (
    get_coverage_from_nodes,
    get_uniqueness_from_nodes,
    get_interestingness_from_nodes,
    get_specificity_from_nodes,
)
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from ..space.Node import VISNode


class ColumbusOracle:
    def __init__(self, weight: OracleWeight) -> None:
        self.weight = weight

    def get_score(
        self, nodes: list["VISNode"], df: pd.DataFrame, wildcard: set[str]
    ) -> OracleResult:
        return OracleResult(
            coverage=get_coverage_from_nodes(nodes, df),
            uniqueness=get_uniqueness_from_nodes(nodes),
            interestingness=get_interestingness_from_nodes(nodes, df),
            specificity=get_specificity_from_nodes(nodes, wildcard),
        )
