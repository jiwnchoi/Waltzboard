from gleaner.model import Attribute
import pandas as pd
from gleaner.oracle import OracleWeight
from collections import Counter


chart_map = [
    ["Q", None, None, "bar", "count"],
    ["Q", None, None, "tick", None],
    ["Q", None, None, "boxplot", None],
    ["N", None, None, "bar", "count"],
    ["N", None, None, "arc", "count"],
    # ["T", None, None, "bar", "count"],
    # ["T", None, None, "arc", "count"],
    # ["T", None, None, "tick", None],
    ["Q", "Q", None, "point", None],
    ["Q", "Q", None, "rect", "count"],
    ["N", "Q", None, "bar", "sum"],
    ["N", "Q", None, "bar", "mean"],
    ["N", "Q", None, "bar", "max"],
    ["N", "Q", None, "bar", "min"],
    ["N", "Q", None, "arc", "sum"],
    ["N", "Q", None, "arc", "mean"],
    ["N", "Q", None, "arc", "max"],
    ["N", "Q", None, "arc", "min"],
    ["N", "Q", None, "tick", None],
    ["N", "Q", None, "boxplot", None],
    # Layered Histogram
    ["Q", "N", None, "bar", "count"],
    # cc heatmap
    ["N", "N", None, "rect", "count"],
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
    ["Q", "Q", "N", "point", None],
    # heatmap bin to q, agg to q
    ["Q", "N", "Q", "rect", "max"],
    ["Q", "N", "Q", "rect", "mean"],
    # Stacked Bar agg to q
    ["N", "Q", "N", "bar", "sum"],
    # Heatmap agg to q
    ["N", "N", "Q", "rect", "mean"],
    ["N", "N", "Q", "rect", "max"],
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
    chart_map: list[list[str | None]]

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
        self.chart_map = chart_map
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
        self.attrs = self.get_attrs()
        self.chart_type = list(set([m[0] for m in chart_map]))
        self.agg_type = list(set([m[-1] for m in chart_map]))
        self.chart_map = chart_map

    def get_attrs(self) -> list[Attribute | None]:
        return [None] + [Attribute(col, "N" if self.df[col].dtype == "object" else "Q") for col in self.attr_names]

    def get_chart_map(self) -> list[list[str | None]]:
        def get_type(counter: Counter, key: str) -> int:
            return counter[key] if key in counter else 0

        filtered_chart_map = [c for c in chart_map if c[0] in self.chart_type and c[4] in self.agg_type]  # type: ignore
        attr_types = [a.type if a is not None else None for a in self.get_attrs()]
        attr_type_counter = Counter(attr_types)
        filtered_chart_map = [
            c
            for c in chart_map
            if get_type(Counter(c), "N") <= attr_type_counter["N"]
            and get_type(Counter(c), "Q") <= attr_type_counter["Q"]
            and get_type(Counter(c), "T") <= attr_type_counter["T"]
        ]
        print(f"filtered_chart_map: {(filtered_chart_map)}")
        return filtered_chart_map

    def update_constraints(self, constraints: list[str]):
        self.init_constraints()
        self.attr_names = [m for m in self.attr_names if m not in constraints]
        self.attrs = self.get_attrs()
        self.chart_type = [m for m in self.chart_type if m not in constraints]
        self.agg_type = [m for m in self.agg_type if m not in constraints]
        self.chart_map = self.get_chart_map()

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
