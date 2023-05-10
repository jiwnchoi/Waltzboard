from dataclasses import dataclass
import pandas as pd
from gleaner.oracle import OracleWeight


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

    def to_dict(self) -> dict[str, float]:
        return {
            "score": self.get_score(),
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "conciseness": self.conciseness,
        }

    def display(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.to_dict(), orient="index", columns=["value"])
