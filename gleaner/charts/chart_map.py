from typing import Literal, Tuple
from gleaner.model.tokens import ChartTokens
from .base_chart import BaseChart
from .bar_chart import SingleBarChart, MultipleBarChart
from .line_chart import LineChart
from .strip_plot import StripPlot
from .scatter_plot import ScatterPlot
from .boxplot import BoxPlot
from .heatmap import Heatmap
from .pie_chart import PieChart

# mark, x, y, z, agg_x, agg_y
chart_map: dict[ChartTokens, BaseChart] = {
    # Bar Chart (Single)
    ("bar", "Q", None, None, "count", None): SingleBarChart,
    ("bar", "T", None, "year", "count", None): SingleBarChart,
    ("bar", "T", None, "month", "count", None): SingleBarChart,
    ("bar", "T", None, "dayofweek", "count", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "mean", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "sum", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "max", None): SingleBarChart,
    ("bar", "N", "Q", None, None, "min", None): SingleBarChart,
    ("bar", "T", "Q", None, "year", "mean", None): SingleBarChart,
    ("bar", "T", "Q", None, "month", "mean", None): SingleBarChart,
    ("bar", "T", "Q", None, "dayofweek", "mean", None): SingleBarChart,
    # Bar Chart (Stacked)
    ("bar", "N", "Q", "N", None, "sum", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "year", "sum", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "month", "sum", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "dayofweek", "sum", None): MultipleBarChart,
    # Bar Chart (Grouped)
    ("bar", "N", "Q", "N", None, "mean", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "year", "mean", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "month", "mean", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "dayofweek", "mean", None): MultipleBarChart,
    ("bar", "N", "Q", "N", None, "max", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "year", "max", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "month", "max", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "dayofweek", "max", None): MultipleBarChart,
    ("bar", "N", "Q", "N", None, "min", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "year", "min", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "month", "min", None): MultipleBarChart,
    ("bar", "T", "Q", "N", "dayofweek", "min", None): MultipleBarChart,
    # Single Line Chart
    ("line", "T", None, None, "year", "count", None): LineChart,
    ("line", "T", None, None, "month", "count", None): LineChart,
    ("line", "T", None, None, "dayofweek", "count", None): LineChart,
    ("line", "T", "Q", None, "year", "mean", None): LineChart,
    ("line", "T", "Q", None, "month", "mean", None): LineChart,
    ("line", "T", "Q", None, "dayofweek", "mean", None): LineChart,
    ("line", "T", "Q", None, "year", "sum", None): LineChart,
    ("line", "T", "Q", None, "month", "sum", None): LineChart,
    ("line", "T", "Q", None, "dayofweek", "sum", None): LineChart,
    ("line", "T", "Q", None, "year", "max", None): LineChart,
    ("line", "T", "Q", None, "month", "max", None): LineChart,
    ("line", "T", "Q", None, "dayofweek", "max", None): LineChart,
    ("line", "T", "Q", None, "year", "min", None): LineChart,
    ("line", "T", "Q", None, "month", "min", None): LineChart,
    ("line", "T", "Q", None, "dayofweek", "min", None): LineChart,
    # Multiple Line Chart
    ("line", "T", "Q", "N", "year", "mean", None): LineChart,
    ("line", "T", "Q", "N", "month", "mean", None): LineChart,
    ("line", "T", "Q", "N", "dayofweek", "mean", None): LineChart,
    ("line", "T", "Q", "N", "year", "sum", None): LineChart,
    ("line", "T", "Q", "N", "month", "sum", None): LineChart,
    ("line", "T", "Q", "N", "dayofweek", "sum", None): LineChart,
    ("line", "T", "Q", "N", "year", "max", None): LineChart,
    ("line", "T", "Q", "N", "month", "max", None): LineChart,
    ("line", "T", "Q", "N", "dayofweek", "max", None): LineChart,
    ("line", "T", "Q", "N", "year", "min", None): LineChart,
    ("line", "T", "Q", "N", "month", "min", None): LineChart,
    ("line", "T", "Q", "N", "dayofweek", "min", None): LineChart,
    # Stripplot
    ("tick", "Q", None, None, None, None): StripPlot,
    ("tick", "Q", "N", None, None, None): StripPlot,
    # Boxplot
    ("boxplot", "Q", None, None, None, None): BoxPlot,
    ("boxplot", "Q", "N", None, None, None): BoxPlot,
    # Pie Chart
    ("arc", "N", None, None, "count", None): PieChart,
    ("arc", "N", "Q", None, "sum", None): PieChart,
    ("arc", "N", "Q", None, "mean", None): PieChart,
    ("arc", "N", "Q", None, "max", None): PieChart,
    ("arc", "N", "Q", None, "min", None): PieChart,
    # Scatter Plot
    ("point", "Q", "Q", None, None, None): ScatterPlot,
    ("point", "Q", "Q", "N", None, None): ScatterPlot,
    ("point", "Q", "Q", "Q", None, None): ScatterPlot,
    # Heatmap
    ("rect", "Q", "Q", None, None, None, "count"): Heatmap,
    ("rect", "N", "N", None, None, None, "count"): Heatmap,
}

chart_map = [
    # cc heatmap
    ("N", "N", None, "rect", "count"),
    # tq
    # colored scatter qqq
    # heatmap agg to xy
    ("Q", "Q", "Q", "rect", "max"),
    ("Q", "Q", "Q", "rect", "mean"),
    # Colored scatter qqc
    # heatmap bin to q, agg to q
    ("Q", "N", "Q", "rect", "max"),
    ("Q", "N", "Q", "rect", "mean"),
    # Stacked Bar agg to q
    ("N", "Q", "N", "bar", "sum"),
    # Heatmap agg to q
    ("N", "N", "Q", "rect", "mean"),
    ("N", "N", "Q", "rect", "max"),
]
