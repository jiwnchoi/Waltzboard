import pandas as pd
import numpy as np
import altair as alt
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from . import (
    Aggregation,
    Filter,
    Sort,
    Binning,
    SingleBar,
    Scatter,
    SingleLine,
    StackedBar,
    MultiLine,
    Heatmap,
    GroupedBar,
    Pie,
    ColoredScatter,
)


if TYPE_CHECKING:
    from space import TransformType, EncodingType


@dataclass
class Attribute:
    name: str
    type: Literal["Q", "N", "T", "O"]
    immutable: bool = False

    def __str__(self):
        return self.name

    def get_copy(self) -> "Attribute":
        return Attribute(self.name, self.type, self.immutable)


class VISNode:
    dim = 0
    attrs: list["Attribute"]
    transforms: list["TransformType"]
    encodings: list["EncodingType"]
    raw_df: pd.DataFrame

    def __init__(self, attrs: list["Attribute"], df: pd.DataFrame):
        self.dim = len(attrs)
        self.attrs = attrs
        self.transforms = []
        self.encodings = []
        self.raw_df = df[[attr.name for attr in attrs]]

    def is_transformable(self) -> bool:
        # check if there is any immutable attribute
        return any([not attr.immutable for attr in self.attrs])

    def get_number_of_types(self) -> dict[Literal["Q", "N", "T", "O"], list[int]]:
        types: dict[Literal["Q", "N", "T", "O"], list[int]] = {
            "Q": [],
            "N": [],
            "O": [],
            "T": [],
        }
        for i in range(len(self.attrs)):
            types[self.attrs[i].type].append(i)
        return types

    def get_copy(self) -> "VISNode":
        return deepcopy(self)

    def print(self):
        print(
            f"dim: {self.dim} attrs: {self.attrs} transforms: {self.transforms} encodings: {self.encodings}"
        )

    def __str__(self) -> str:
        return f"dim: {self.dim} attrs: {self.attrs} transforms: {self.transforms} encodings: {self.encodings}"


class Visualizations:
    def __init__(self, node: "VISNode", encoding: EncodingType) -> None:
        self.attrs = node.attrs
        self.transforms = node.transforms
        self.encoding = encoding
        self.raw_df = node.raw_df

    def __str__(self) -> str:
        return f"encoding: {self.encoding} attrs: {self.attrs} transforms: {self.transforms}"

    def get_df(self) -> pd.DataFrame:
        df = self.raw_df.copy()
        for transform in self.transforms:
            if isinstance(transform, Aggregation):
                df = df.groupby(transform.by).agg(transform.type)
            elif isinstance(transform, Filter):
                df = df[df[transform.by] == transform.value]
            elif isinstance(transform, Sort):
                df = df.sort_values(
                    by=transform.by,
                    ascending=True if transform.type == "asc" else False,
                )
            elif isinstance(transform, Binning):
                N = df[transform.by].count()
                step = min(int(N / 6), 1)
                bin_edges = df[transform.by].sort_values().unique()[::step]
                round_edges = np.round(
                    bin_edges, -int(np.log10(bin_edges[1] - bin_edges[0]))
                ).tolist()
                df[transform.by] = pd.cut(
                    df[transform.by],
                    bins=round_edges,
                    labels=round_edges[:-1],
                    right=False,
                )
        return df
