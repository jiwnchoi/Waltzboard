class OracleWeight:
    coverage: float = 1.0
    uniqueness: float = 1.0
    specificity: float = 1.0
    interestingness: float = 1.0

    def __init__(self, task="none") -> None:
        if task == "quantitative":
            self.specificity = 3.0
            self.uniqueness = 0.5

        elif task == "qualitative":
            self.specificity = 3.0
            self.interestingness = 3.0

        elif task == "exploratory":
            self.coverage = 3.0
            self.uniqueness = 3.0

        elif task == "predictive":
            self.coverage = 3.0
            self.interestingness = 3.0
