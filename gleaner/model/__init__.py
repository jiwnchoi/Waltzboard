from typing import Literal


AttrTypes = Literal["Q", "N", "T"] | None
MarkTypes = Literal["bar", "arc", "tick", "point", "rect", "line", "boxplot"]
TrsTypes = Literal["bin", "count", "sum", "mean", "max", "min", None]
TrsXTypes = TrsTypes | Literal["year", "month", "day", "bin"]
ChartTokens = tuple[MarkTypes, str, str | None, str | None, TrsXTypes, TrsTypes, TrsTypes]
ChartKeyTokens = tuple[MarkTypes, AttrTypes, AttrTypes, AttrTypes, TrsXTypes, TrsTypes, TrsTypes]
from .attribute import Attribute

ChartSampled = tuple[MarkTypes, Attribute, Attribute, Attribute, TrsXTypes, TrsTypes, TrsTypes]

from .gleaner_chart import *
from .charts import BaseChart
from .chart_map import *
from .gleaner_dahsboard import GleanerDashboard
