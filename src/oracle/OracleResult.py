from typing import TYPE_CHECKING
from dataclasses import dataclass
import altair as alt
from altair import Chart


from . import OracleWeight

if TYPE_CHECKING:
    from src.model.Node import VisualizationNode


@dataclass
class OracleResult:
    weight: OracleWeight
    coverage: float
    diversity: float
    specificity: float
    interestingness: float
    conciseness: float
    dashboard: list["VisualizationNode"]

    def get_score(self) -> float:
        return (
            self.weight.coverage * self.coverage
            + self.weight.diversity * self.diversity
            + self.weight.interestingness * self.interestingness
            + self.weight.specificity * self.specificity
            + self.weight.conciseness * self.conciseness
        )

    def __str__(self) -> str:
        return f"""
Score: {self.get_score()}
Coverage: {self.coverage}
diversity: {self.diversity}
Specificity: {self.specificity}
Interestingness: {self.interestingness}
Conciseness: {self.conciseness}
        """

    def to_dict(self) -> dict[str, float]:
        return {
            "score": self.get_score(),
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "conciseness": self.conciseness,
        }

    def display_dashboard(self, size, num_cols):
        if self.dashboard is None:
            return None

        altairs = [
            node.get_altair().properties(width=size, height=size)
            for node in self.dashboard
        ]
        rows: list[alt.HConcatChart] = [
            alt.hconcat(*altairs[i : i + num_cols]).resolve_scale(color="independent")
            for i in range(0, len(altairs), num_cols)
        ]
        return alt.vconcat(*rows)
