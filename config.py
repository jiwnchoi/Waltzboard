from typing import Literal

MAX_TARGET_ATTRIBUTES = 4
FILTER_VALUE_THRESHOLD = 10
EncodingType = Literal["bar", "line", "area", "pie", "scatter", "box", "heatmap"]
AggregationType = Literal["max", "min", "mean", "count", "sum"]
MAX_BINS = 10
MIN_ROWS = 4
MAX_UNIQUE_CATEGORY = 10
MAX_UNIQUE_AXIS = 20
