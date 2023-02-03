from typing import Literal

MAX_TARGET_ATTRIBUTES = 4
FILTER_VALUE_THRESHOLD = 10
EncodingType = Literal["bar", "line", "area", "pie", "scatter", "box", "heatmap"]
AggregationType = Literal["max", "min", "mean", "count", "sum"]
