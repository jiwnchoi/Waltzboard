from typing import Literal, Tuple
from .attribute import AttrTypes
from .data_transforms import AggTypes, AggXTypes

MarkTypes = Literal["bar", "arc", "tick", "point", "rect", "line", "boxplot"]

AllTokenTypes = MarkTypes | AttrTypes | AggTypes | AggXTypes
ChartTokens = tuple[MarkTypes, AttrTypes, AttrTypes, AttrTypes, AggXTypes, AggTypes, AggTypes]
