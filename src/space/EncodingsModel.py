from dataclasses import dataclass
from .DataModel import Attribute
from typing import Union
import altair as alt
import pandas as pd


@dataclass
class SingleBar:
    x: Attribute
    y: Attribute
    mark = "bar"

    def __str__(self) -> str:
        return f"SingleBar({self.x.name}, {self.y.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_bar()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
            )
        )


@dataclass
class SingleLine:
    x: Attribute
    y: Attribute
    mark = "line"

    def __str__(self) -> str:
        return f"SingleLine({self.x.name}, {self.y.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_line()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
            )
        )


@dataclass
class Scatter:
    x: Attribute
    y: Attribute
    mark = "circle"

    def __str__(self) -> str:
        return f"Scatter({self.x.name}, {self.y.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_circle()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
            )
        )


@dataclass
class Pie:
    color: Attribute
    theta: Attribute
    mark = "arc"

    def __str__(self) -> str:
        return f"Pie({self.color.name}, {self.theta.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_arc()
            .encode(
                theta=f"{self.theta.name}:{self.theta.type}",
                color=f"{self.color.name}:{self.color.type}",
            )
        )


# 3D Encoding
@dataclass
class Heatmap:
    x: Attribute
    y: Attribute
    color: Attribute
    mark = "rect"

    def __str__(self) -> str:
        return f"Heatmap({self.x.name}, {self.y.name}, {self.color.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_rect()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
                color=f"{self.color.name}:{self.color.type}",
            )
        )


@dataclass
class GroupedBar:
    x: Attribute
    y: Attribute
    group: Attribute
    mark = "bar"

    def __str__(self) -> str:
        return f"GroupedBar({self.x.name}, {self.y.name}, {self.group.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_bar()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
                column=f"{self.group.name}:{self.group.type}",
            )
        )


@dataclass
class StackedBar:
    x: Attribute
    y: Attribute
    color: Attribute
    mark = "bar"

    def __str__(self) -> str:
        return f"StackedBar({self.x.name}, {self.y.name}, {self.color.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_bar()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
                color=f"{self.color.name}:{self.color.type}",
            )
        )


@dataclass
class ColoredScatter:
    x: Attribute
    y: Attribute
    color: Attribute
    mark = "circle"

    def __str__(self) -> str:
        return f"ColoredScatter({self.x.name}, {self.y.name}, {self.color.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_circle()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
                color=f"{self.color.name}:{self.color.type}",
            )
        )


@dataclass
class MultiLine:
    x: Attribute
    y: Attribute
    color: Attribute
    mark = "line"

    def __str__(self) -> str:
        return f"MultiLine({self.x.name}, {self.y.name}, {self.color.name})"

    def get_altair(self, df: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(df)  # type: ignore
            .mark_line()
            .encode(
                x=f"{self.x.name}:{self.x.type}",
                y=f"{self.y.name}:{self.y.type}",
                color=f"{self.color.name}:{self.color.type}",
            )
        )


EncodingType = Union[
    Scatter,
    SingleBar,
    SingleLine,
    Heatmap,
    Pie,
    StackedBar,
    GroupedBar,
    ColoredScatter,
    MultiLine,
]
