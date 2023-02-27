from dataclasses import dataclass
from typing import Literal, Optional, Any
import pandas as pd


@dataclass
class Attribute:
    name: str
    type: Literal["Q", "N", "T", "O"]
    immutable: bool = False

    def __str__(self):
        return self.name

    def get_copy(self) -> "Attribute":
        return Attribute(self.name, self.type, self.immutable)

    def get_long_type(self) -> str:
        return {
            "Q": "quantitative",
            "N": "nominal",
            "T": "temporal",
            "O": "ordinal",
        }[self.type]


@dataclass
class VisualizableDataFrame:
    df: pd.DataFrame
    attrs: tuple["Attribute", ...]
    filter: Optional[tuple[tuple[str, Any, Any]]]
