from typing import Literal

from .attribute import Attribute

AttrTypes = Literal["Q", "N", "T"] | None
MarkTypes = Literal["bar", "arc", "tick", "point", "rect", "line", "boxplot"]
TrsTypes = Literal["bin", "count", "sum", "mean", "max", "min", None]
TrsXTypes = TrsTypes | Literal["year", "month", "day", "bin"]
ChartTokens = tuple[
    MarkTypes, str, str | None, str | None, TrsXTypes, TrsTypes, TrsTypes
]
ChartKeyTokens = tuple[
    MarkTypes, AttrTypes, AttrTypes, AttrTypes, TrsXTypes, TrsTypes, TrsTypes
]

ChartSampled = tuple[
    MarkTypes, Attribute, Attribute, Attribute, TrsXTypes, TrsTypes, TrsTypes
]

all = [
    "ChartTokens",
    "ChartKeyTokens",
    "ChartSampled",
]
