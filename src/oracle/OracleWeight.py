from dataclasses import dataclass


@dataclass
class OracleWeight:
    coverage: float = 1.0
    diversity: float = 1.0
    specificity: float = 1.0
    interestingness: float = 1.0
    conciseness: float = 1.0

    def to_dict(self) -> dict[str, float]:
        return {
            "coverage": self.coverage,
            "diversity": self.diversity,
            "specificity": self.specificity,
            "interestingness": self.interestingness,
            "conciseness": self.conciseness,
        }
