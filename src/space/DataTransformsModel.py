from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class Aggregation:
    by: list[str]
    type: Literal["max", "min", "mean", "count", "sum"]


@dataclass
class Filter:
    by: str
    value: Union[str, int, float]
    type: Literal["eq", "neq"]


@dataclass
class Sort:
    by: str
    type: Literal["asc", "desc"]


@dataclass
class Binning:
    by: str
    type: Literal["bin"] = "bin"


TransformType = Union[Aggregation, Filter, Sort, Binning]
