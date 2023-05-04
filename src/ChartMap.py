from dataclasses import dataclass
from typing import Union
import altair as alt

# Q C T

chart_map = [
    ["Q", None, None, "bar", "count"],
    ["Q", None, None, "tick", None],
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


chart_type = list(set([m[0] for m in chart_map]))
agg_type = list(set([m[-1] for m in chart_map]))
