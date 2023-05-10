from dataclasses import dataclass
import altair as alt
from typing import Literal


@dataclass
class Encodings:
    chart_type: str
    x: alt.X | alt.Color
    y: alt.Y | alt.Theta | None = None
    z: alt.Color | alt.Column | alt.Y | None = None