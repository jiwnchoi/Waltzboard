from dataclasses import dataclass
from typing import Literal, Optional, Any
import pandas as pd


@dataclass
class Attribute:
    name: str
    type: Literal["Q", "C", "T", "O", "N", "N"]

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name, "type": self.type}

    def long_type(self):
        return {
            "Q": "quantitative",
            "C": "nominal",
            "T": "temporal",
            "O": "ordinal",
            "N": "name",
        }[self.type]


@dataclass
class VisualizableDataFrame:
    df: pd.DataFrame
    attrs: list["Attribute"]
    filter: Optional[list[tuple[str, Any, Any]]]

