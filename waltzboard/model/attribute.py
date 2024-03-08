from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .const import AttrTypes


@dataclass
class Attribute:
    name: str | None
    type: "AttrTypes"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name, "type": self.type}

    def long_type(self) -> Literal["quantitative", "nominal", "temporal", None]:
        return {
            "Q": "quantitative",
            "N": "nominal",
            "T": "temporal",
            None: None,
        }[self.type]
