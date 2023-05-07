from dataclasses import dataclass
from typing import Literal, Union
from .attribute import Attribute


@dataclass
class Aggregation:
    by: list[str]
    # ["max", "min", "mean", "count", "sum"]
    type: str
    name = "agg"


@dataclass
class Filter:
    by: Union[str, Attribute]
    value: Union[str, int, float]
    type: Literal["eq", "neq"]
    name = "filter"


@dataclass
class Sort:
    by: str
    type: Literal["asc", "desc"]
    name: str = "sort"


@dataclass
class Binning:
    by: str
    type: Literal["bin"] = "bin"
    name = "bin"


TransformType = Aggregation | Filter | Sort | Binning
