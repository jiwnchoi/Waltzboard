from dataclasses import dataclass, field
from src.oracle import OracleWeight


@dataclass
class OracleResult:
    weight: OracleWeight
    coverage: float
    uniqueness: float
    specificity: float
    interestingness: float

    def get_score(self) -> float:
        return (
            self.weight.coverage * self.coverage
            + self.weight.uniqueness * self.uniqueness
            + self.weight.interestingness * self.interestingness
            + self.weight.specificity * self.specificity
        )

    def __str__(self) -> str:
        return f"""
Coverage: {self.coverage}
Uniqueness: {self.uniqueness}
Specificity: {self.specificity}
Interestingness: {self.interestingness}
        """
