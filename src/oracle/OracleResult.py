from dataclasses import dataclass, field
from src.oracle import OracleWeight


@dataclass
class OracleResult:
    coverage: float
    uniqueness: float
    specificity: float
    interestingness: float

    def get_score(self, weight: OracleWeight) -> float:
        return (
            weight.coverage * self.coverage
            + weight.uniqueness * self.uniqueness
            + weight.interestingness * self.interestingness
            + weight.specificity * self.specificity
        )
