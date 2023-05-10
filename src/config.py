from src.model import Attribute
import pandas as pd


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
    chart_type: list[str]
    agg_type: list[str]
    chart_map: list[list[str | None]] = chart_map

    # Explorer config
    n_epoch: int
    n_candidates: int
    halving_ratio: float

    def __init__(
        self,
        df: pd.DataFrame,
        robustness: int = 150,
        n_epoch: int = 50,
        n_candidates: int = 100,
        halving_ratio: float = 0.1,
    ) -> None:
        self.robustness = robustness
        self.n_epoch = n_epoch
        self.n_candidates = n_candidates
        self.halving_ratio = halving_ratio

        self.df = df
        self.attr_names = [
            col
            for col in df.columns
            if (df[col].dtype == "object" and df[col].nunique() < 10)
            or df[col].dtype != "object"
        ]
        self.attrs: list[Attribute] = [
            Attribute(col, "C" if df[col].dtype == "object" else "Q")
            for col in self.attr_names
        ]
        self.chart_type = list(set([m[0] for m in chart_map]))
        self.agg_type = list(set([m[-1] for m in chart_map]))

    def constraint(self, constraint: list[str]):
        self.attr_names = [m for m in self.attr_names if m not in constraint]
        self.chart_type = [m for m in self.chart_type if m not in constraint]
        self.agg_type = [m for m in self.agg_type if m not in constraint]
