from dataclasses import dataclass
from typing import Literal, Union
from .attribute import Attribute

AggTypes = Literal["count", "sum", "mean", "max", "min", None]
AggXTypes = AggTypes | Literal["year", "month", "dayofweek"]
