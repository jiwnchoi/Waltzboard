from dataclasses import dataclass, field


@dataclass
class OracleWeight:
    coverage: float = 1.0
    uniqueness: float = 1.0
    specificity: float = 1.0
    interestingness: float = 1.0


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
