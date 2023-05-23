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
    parsimony: float

    def get_score(self) -> float:
        return (
            self.weight.coverage * self.coverage
            + self.weight.diversity * self.diversity
            + self.weight.interestingness * self.interestingness
            + self.weight.specificity * self.specificity
            + self.weight.parsimony * self.parsimony
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "score": self.get_score(),
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "parsimony": self.parsimony,
        }

    def display(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.to_dict(), orient="index", columns=["value"])
