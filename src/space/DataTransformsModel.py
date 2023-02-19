from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class Aggregation:
    by: list[str]
    type: Literal["max", "min", "mean", "count", "sum"]
    name = "agg"


@dataclass
class Filter:
    by: str
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


TransformType = Union[Aggregation, Filter, Sort, Binning]
