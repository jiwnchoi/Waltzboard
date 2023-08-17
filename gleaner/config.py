from gleaner.model import Attribute
import pandas as pd
from gleaner.oracle import OracleWeight


chart_map = [
    ["Q", None, None, "bar", "count"],
    ["Q", None, None, "tick", None],
    ["Q", None, None, "boxplot", None],
    ["C", None, None, "bar", "count"],
    ["C", None, None, "arc", "count"],
    ["T", None, None, "bar", "count"],
    ["T", None, None, "arc", "count"],
    ["T", None, None, "tick", None],
    ["Q", "Q", None, "point", None],
    ["Q", "Q", None, "rect", "count"],
    ["C", "Q", None, "bar", "sum"],
    ["C", "Q", None, "bar", "mean"],
    ["C", "Q", None, "bar", "max"],
    ["C", "Q", None, "bar", "min"],
    ["C", "Q", None, "arc", "sum"],
    ["C", "Q", None, "arc", "mean"],
    ["C", "Q", None, "arc", "max"],
    ["C", "Q", None, "arc", "min"],
    ["C", "Q", None, "tick", None],
    ["C", "Q", None, "boxplot", None],
    # Layered Histogram
    ["Q", "C", None, "bar", "count"],
    # cc heatmap
    ["C", "C", None, "rect", "count"],
    # tq
    # ["T", "Q", None, "line", "max"],
    # ["T", "Q", None, "line", "mean"],
    # ["T", "Q", None, "line", "sum"],
    # ["T", "Q", None, "line", "min"],
    # colored scatter qqq
    ["Q", "Q", "Q", "point", None],
    # heatmap agg to xy
    ["Q", "Q", "Q", "rect", "max"],
    ["Q", "Q", "Q", "rect", "mean"],
    # Colored scatter qqc
    ["Q", "Q", "C", "point", None],
    # heatmap bin to q, agg to q
    ["Q", "C", "Q", "rect", "max"],
    ["Q", "C", "Q", "rect", "mean"],
    # Stacked Bar agg to q
    ["C", "Q", "C", "bar", "sum"],
    # Heatmap agg to q
    ["C", "C", "Q", "rect", "mean"],
    ["C", "C", "Q", "rect", "max"],
]

for c in chart_map:
    mark = c.pop(3)
    c.insert(0, mark)


class GleanerConfig:
    # Generator config
    robustness: int
    attr_names: list[str]
    chart_type: list[str]
    agg_type: list[str]
    chart_map: list[list[str | None]] = chart_map

    # Explorer config
    n_epoch: int = 50
    n_candidates: int = 100
    n_search_space: int = 100
    n_beam: int = 10
    halving_ratio: float = 0.1

    # Oracle Config
    weight: OracleWeight

    def __init__(
        self,
        df: pd.DataFrame,
        robustness: int = 100,
        n_epoch: int = 50,
        n_candidates: int = 100,
        halving_ratio: float = 0.1,
    ) -> None:
        self.robustness = robustness
        self.n_epoch = n_epoch
        self.n_candidates = n_candidates
        self.halving_ratio = halving_ratio
        self.df = df
        self.weight = OracleWeight()
        self.init_constraints()

    def init_constraints(self):
        self.attr_names = [
            col
            for col in self.df.columns
            if (self.df[col].dtype == "object" and self.df[col].nunique() < 10) or self.df[col].dtype != "object"
        ]
        self.df = self.df[self.attr_names]
        self.attrs: list[Attribute] = [
            Attribute(col, "C" if self.df[col].dtype == "object" else "Q") for col in self.attr_names
        ]
        self.chart_type = list(set([m[0] for m in chart_map]))
        self.agg_type = list(set([m[-1] for m in chart_map]))

    def update_constraints(self, constraints: list[str]):
        self.attr_names = [m for m in self.attr_names if m not in constraints]
        self.chart_type = [m for m in self.chart_type if m not in constraints]
        self.agg_type = [m for m in self.agg_type if m not in constraints]

    def update_weight(
        self,
        specificity: float | None = None,
        interestingness: float | None = None,
        coverage: float | None = None,
        diversity: float | None = None,
        parsimony: float | None = None,
    ):
        if specificity is not None:
            self.weight.specificity = specificity
        if interestingness is not None:
            self.weight.interestingness = interestingness
        if coverage is not None:
            self.weight.coverage = coverage
        if diversity is not None:
            self.weight.diversity = diversity
        if parsimony is not None:
            self.weight.parsimony = parsimony
