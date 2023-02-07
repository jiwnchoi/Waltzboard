import pandas as pd
import numpy as np
import altair as alt
from copy import deepcopy
from typing import TYPE_CHECKING, Literal

from .DataTransformsModel import Aggregation, Filter, Sort, Binning, TransformType
from .EncodingsModel import EncodingType

from config import MAX_BINS, MIN_ROWS
from typing import Union

if TYPE_CHECKING:
    from .DataModel import Attribute


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
        self.df = self.raw_df

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

    def get_df(self) -> Union[pd.DataFrame, None]:
        df = self.raw_df.copy()
        # print(df)
        for transform in self.transforms:
            if len(df.dropna()) < MIN_ROWS:
                return None

            # print(transform)
            if isinstance(transform, Aggregation):
                if transform.type == "count":
                    df = df.groupby(transform.by).size().reset_index(name=f"count")

                df = df.groupby(transform.by).agg(transform.type).reset_index()
            elif isinstance(transform, Filter):
                df = df[df[transform.by] == transform.value]
                df = df.drop(columns=transform.by)
            elif isinstance(transform, Sort):
                df = df.sort_values(
                    by=transform.by,
                    ascending=True if transform.type == "asc" else False,
                )
            elif isinstance(transform, Binning):
                N = df[transform.by].count()
                MAX_BINS = 10
                num_bins = min(MAX_BINS, N)
                unique_values = df[transform.by].sort_values().unique()

                step = (
                    int(len(unique_values) / num_bins)
                    if len(unique_values) > num_bins
                    else 1
                )
                bin_edges = unique_values[::step]

                labels = [
                    [bin_edges[i], bin_edges[i + 1]] for i in range(len(bin_edges) - 1)
                ]
                labels[0][0] = min(unique_values)
                labels[-1][1] = max(unique_values)
                labels = [f"{label[0]}-{label[1]}" for label in labels]

                df[transform.by] = pd.cut(
                    df[transform.by],
                    bins=bin_edges.tolist(),
                    right=True,
                    labels=labels,
                    duplicates="raise",
                    include_lowest=True,
                    precision=0,
                )  # type: ignore
            self.df = df
        return df

    def get_altair(self) -> list[alt.Chart]:
        df = self.get_df()
        if df is None:
            return []
        return [encoding.get_altair(df) for encoding in self.encodings]

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
