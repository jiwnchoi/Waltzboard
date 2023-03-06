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


@dataclass
class VisualizableDataFrame:
    df: pd.DataFrame
    attrs: tuple["Attribute", ...]
    filter: Optional[tuple[tuple[str, Any, Any]]]
