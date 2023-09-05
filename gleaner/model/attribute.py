from dataclasses import dataclass
from typing import Literal

AttrTypes = Literal["Q", "N", "T", None]


@dataclass
class Attribute:
    name: str
    type: Types

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name, "type": self.type}

    def long_type(self):
        return {
            "Q": "quantitative",
            "N": "nominal",
            "T": "temporal",
            "N": "name",
        }[self.type]
