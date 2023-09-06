from typing import Literal


AttrTypes = Literal["Q", "N", "T"] | None
MarkTypes = Literal["bar", "arc", "tick", "point", "rect", "line", "boxplot"]
AggTypes = Literal["count", "sum", "mean", "max", "min", None]
AggXTypes = AggTypes | Literal["year", "month", "dayofweek"]
ChartTokens = tuple[MarkTypes, str, str | None, str | None, AggXTypes, AggTypes, AggTypes]
ChartKeyTokens = tuple[MarkTypes, AttrTypes, AttrTypes, AttrTypes, AggXTypes, AggTypes, AggTypes]
from .attribute import Attribute

ChartSampled = tuple[MarkTypes, Attribute, Attribute, Attribute, AggXTypes, AggTypes, AggTypes]

from .gleaner_chart import (
    get_chart_from_sample,
    get_chart_from_tokens,
)
from .charts import BaseChart
from .chart_map import *
from .gleaner_dahsboard import GleanerDashboard
