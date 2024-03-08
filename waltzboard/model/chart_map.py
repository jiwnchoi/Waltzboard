from .charts import (
    BoxPlot,
    Heatmap,
    LineChart,
    MultipleBarChart,
    PieChart,
    ScatterPlot,
    SingleBarChart,
    StripPlot,
)
from .const import ChartKeyTokens

ChartMapType = dict[ChartKeyTokens, type]

ChartMap: ChartMapType = {
    # Bar Chart (Single)
    ("bar", "Q", None, None, "bin", "count", None): SingleBarChart,
    ("bar", "N", None, None, None, "count", None): SingleBarChart,
    ("bar", "T", None, None, "year", "count", None): SingleBarChart,
    ("bar", "T", None, None, "month", "count", None): SingleBarChart,
    ("bar", "T", None, None, "day", "count", None): SingleBarChart,
    # Single Bar Chart
    ("bar", "N", "Q", None, None, "mean", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "sum", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "max", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "min", None): SingleBarChart,
    ("bar", "T", "Q", None, "year", "mean", None): SingleBarChart,
    ("bar", "T", "Q", None, "month", "mean", None): SingleBarChart,
    ("bar", "T", "Q", None, "day", "mean", None): SingleBarChart,
    # Stripplot
    ("tick", "Q", None, None, None, None, None): StripPlot,
    ("tick", "N", "Q", None, None, None, None): StripPlot,
    # Boxplot
    ("boxplot", "Q", None, None, None, None, None): BoxPlot,
    ("boxplot", "N", "Q", None, None, None, None): BoxPlot,
    # Scatter Plot
    ("point", "Q", "Q", None, None, None, None): ScatterPlot,
    ("point", "Q", "Q", "N", None, None, None): ScatterPlot,
    ("point", "Q", "Q", "Q", None, None, None): ScatterPlot,
}


for t_x in ["year", "month", "day"]:
    for t_y in ["mean", "max", "min", "sum"]:
        ChartMap[("bar", "T", "Q", None, t_x, t_y, None)] = SingleBarChart

# write code that iteratively adding heatmaps
for x in ["T", "Q", "N"]:
    for y in ["T", "Q", "N"]:
        for z in ["Q", None]:
            for a in (
                ["year", "month", "day"]
                if x == "T"
                else ["bin"]
                if x == "Q"
                else [None]
            ):
                for b in (
                    ["year", "month", "day"]
                    if y == "T"
                    else ["bin"]
                    if y == "Q"
                    else [None]
                ):
                    for c in (
                        ["count"] if (z is None) else ["mean", "max", "min", "sum"]
                    ):
                        ChartMap[("rect", x, y, z, a, b, c)] = Heatmap

# Write code that iteratively adding pie charts
for y in ["Q", None]:
    for agg_y in ["sum", "mean", "max", "min", "count"]:
        if y is None:
            ChartMap[("arc", "N", y, None, None, agg_y, None)] = PieChart
        else:
            ChartMap[("arc", "N", y, None, None, agg_y, None)] = PieChart


# Write code that iteratively adding line chart
for agg_x in ["year", "month", "day"]:
    for y in [None, "Q"]:
        if y is None:
            ChartMap[("line", "T", y, None, agg_x, "count", None)] = LineChart
            continue
        for z in ["N", None]:
            for agg_y in ["mean", "max", "min", "sum"]:
                ChartMap[("line", "T", y, z, agg_x, agg_y, None)] = LineChart

# multiple bar chart
for x in ["T", "N"]:
    if x == "T":
        for agg_x in ["year", "month", "day"]:
            for agg_y in ["mean", "max", "min", "sum"]:
                ChartMap[("bar", x, "Q", "N", agg_x, agg_y, None)] = MultipleBarChart
    else:
        for agg_y in ["mean", "max", "min", "sum"]:
            ChartMap[("bar", x, "Q", "N", None, agg_y, None)] = MultipleBarChart


__all__ = ["ChartMap", "ChartMapType"]
