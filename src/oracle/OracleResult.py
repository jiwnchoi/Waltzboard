from dataclasses import dataclass
from . import OracleWeight


@dataclass
class OracleResult:
    weight: OracleWeight
    coverage: float
    diversity: float
    specificity: float
    interestingness: float
    conciseness: float

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
