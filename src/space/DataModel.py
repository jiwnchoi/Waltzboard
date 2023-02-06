from dataclasses import dataclass
from typing import Literal


@dataclass
class Attribute:
    name: str
    type: Literal["Q", "N", "T", "O"]
    immutable: bool = False

    def __str__(self):
        return self.name

    def get_copy(self) -> "Attribute":
        return Attribute(self.name, self.type, self.immutable)
