import pandas as pd
import numpy as np
import altair as alt
from copy import deepcopy
from typing import TYPE_CHECKING, Literal, Set, Optional

from .DataTransformsModel import Aggregation, Filter, Sort, Binning, TransformType

from config import MAX_BINS, MIN_ROWS
from typing import Union

from dataclasses import dataclass

if TYPE_CHECKING:
    from .DataModel import Attribute


chart_type = Literal["bar", "line", "circle", "area", "arc", "rect"]


@dataclass
class Encodings:
    chart_type: str
    x: Union[alt.X, alt.Color]
    y: Union[alt.Y, alt.Theta]
    z: Union[alt.Color, alt.Column, alt.Y, None] = None


@dataclass
class VisualizationNode:
    sub_df: pd.DataFrame
    attrs: tuple["Attribute"]

    filters: Optional[tuple[tuple[str, str, str]]]
    binnings: Optional[list["Binning"]]
    aggregation: Optional["Aggregation"]

    encoding: Optional["Encodings"]

    chart: Optional[alt.Chart]

    def get_children(self) -> list["VisualizationNode"]:
        filtered_attrs = [
            attr for attr in self.attrs if self.sub_df[attr.name].nunique() != 1
        ]
        dim = len(filtered_attrs)

        children: list["VisualizationNode"] = []
        types = self.get_number_of_types()

        if dim == 1 and filtered_attrs[0].type == "N":
            for encoding in ["bar", "arc"]:
                child = deepcopy(self)
                child.aggregation = Aggregation(by=[types["N"][0].name], type="count")
                child.encoding = Encodings(
                    encoding,
                    alt.X(field=types["N"][0].name, type="nominal"),  # type: ignore
                    alt.Y(field=types["N"][0].name, aggregate="count", type="nominal"),  # type: ignore
                )
                children.append(child)

        elif dim == 1 and filtered_attrs[0].type == "Q":
            for agg in ["count", "sum", "mean"]:
                child = deepcopy(self)
                child.binnings = [Binning(by=types["Q"][0].name)]
                child.aggregation = Aggregation(by=[types["Q"][0].name], type=agg)
                child.encoding = Encodings(
                    "bar",
                    alt.X(field=types["Q"][0].name, type="quantitative"),  # type: ignore
                    alt.Y(field=types["Q"][0].name, aggregate=agg, type="quantitative"),  # type: ignore
                )
                children.append(child)

        # QQ
        elif dim == 2 and len(types["Q"]) == 2:
            # Scatterplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "circle",
                alt.X(field=types["Q"][0].name, type="quantitative"),  # type: ignore
                alt.Y(field=types["Q"][1].name, type="quantitative"),  # type: ignore
            )
            children.append(child)

            # Heatmap
            child = deepcopy(self)
            child.binnings = [
                Binning(by=types["Q"][0].name),
                Binning(by=types["Q"][1].name),
            ]
            child.aggregation = Aggregation(
                by=[types["Q"][0].name, types["Q"][1].name], type="count"
            )
            child.encoding = Encodings(
                "rect",
                alt.X(field=types["Q"][0].name, type="quantitative", bin=True),  # type: ignore
                alt.Y(field=types["Q"][1].name, type="quantitative", bin=True),  # type: ignore
                alt.Color(aggregate="count", type="quantitative"),  # type: ignore
            )
            children.append(child)

        # QN
        elif dim == 2 and len(types["Q"]) == 1 and len(types["N"]) == 1:
            # Bar
            for agg in ["sum", "mean", "max", "min"]:
                child = deepcopy(self)
                child.aggregation = Aggregation(by=[types["N"][0].name], type=agg)
                child.encoding = Encodings(
                    "bar",
                    alt.X(field=types["N"][0].name, type="nominal"),  # type: ignore
                    alt.Y(field=types["Q"][0].name, type="quantitative", aggregate=agg),  # type: ignore
                )
                children.append(child)

            # Pie
            # for agg in ["sum", "mean", "max", "min"]:
            #     child = deepcopy(self)
            #     child.aggregation = Aggregation(by=[types["N"][0].name], type=agg)
            #     child.encoding = Encodings(
            #         "arc",
            #         alt.Color(field=types["N"][0].name, type="nominal"),  # type: ignore
            #         alt.Theta(field=types["Q"][0].name, type="quantitative", aggregate=agg),  # type: ignore
            #     )
            #     children.append(child)

        # NN
        elif dim == 2 and len(types["N"]) == 2:
            # Heatmap
            child = deepcopy(self)
            child.aggregation = Aggregation(
                by=[types["N"][0].name, types["N"][1].name], type="count"
            )
            child.encoding = Encodings(
                "rect",
                alt.X(field=types["N"][0].name, type="nominal"),  # type: ignore
                alt.Y(field=types["N"][1].name, type="nominal"),  # type: ignore
                alt.Color(aggregate="count", type="quantitative"),  # type: ignore
            )
            children.append(child)

        # QQQ
        elif dim == 3 and len(types["Q"]) == 3:
            # Colored Scatterplot
            for i in range(3):
                child = deepcopy(self)
                child.binnings = [Binning(by=types["Q"][i].name)]
                child.encoding = Encodings(
                    "circle",
                    alt.X(field=types["Q"][i].name, type="quantitative"),  # type: ignore
                    alt.Y(field=types["Q"][(i + 1) % 3].name, type="quantitative"),  # type: ignore
                    alt.Color(field=types["Q"][(i + 2) % 3].name, type="quantitative", bin=True),  # type: ignore
                )
                children.append(child)

            # Heatmap
            for i in range(3):
                for agg in ["mean", "max"]:
                    child = deepcopy(self)
                    child.binnings = [
                        Binning(by=types["Q"][i].name),
                        Binning(by=types["Q"][(i + 1) % 3].name),
                    ]
                    child.encoding = Encodings(
                        "rect",
                        alt.X(field=types["Q"][i].name, type="quantitative", bin=True),  # type: ignore
                        alt.Y(field=types["Q"][(i + 1) % 3].name, type="quantitative", bin=True),  # type: ignore
                        alt.Color(field=types["Q"][(i + 2) % 3].name, type="quantitative", aggregate=agg),  # type: ignore
                    )
                    children.append(child)

        # QQN
        elif dim == 3 and len(types["Q"]) == 2 and len(types["N"]) == 1:
            # Colored Scatterplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "circle",
                alt.X(field=types["Q"][0].name, type="quantitative"),  # type: ignore
                alt.Y(field=types["Q"][1].name, type="quantitative"),  # type: ignore
                alt.Color(field=types["N"][0].name, type="nominal"),  # type: ignore
            )
            children.append(child)

            # Heatmap
            for i in range(2):
                for agg in ["mean", "max"]:
                    child = deepcopy(self)
                    child.binnings = [Binning(by=types["Q"][i].name)]
                    child.encoding = Encodings(
                        "rect",
                        alt.X(field=types["Q"][i].name, type="quantitative", bin=True),  # type: ignore
                        alt.Y(field=types["N"][0].name, type="nominal"),  # type: ignore
                        alt.Color(field=types["Q"][1 - i].name, type="quantitative", aggregate=agg),  # type: ignore
                    )
                    children.append(child)

        # QNN
        elif dim == 3 and len(types["Q"]) == 1 and len(types["N"]) == 2:
            # Stacked Bar
            for i in range(2):
                for agg in ["count", "sum", "mean", "max", "min"]:
                    child = deepcopy(self)
                    child.aggregation = Aggregation(
                        by=[types["N"][0].name, types["N"][1].name], type=agg
                    )
                    child.encoding = Encodings(
                        "stacked_bar",
                        alt.X(field=types["N"][i].name, type="nominal"),  # type: ignore
                        alt.Y(field=types["Q"][0].name, type="quantitative", aggregate=agg),  # type: ignore
                        alt.Color(field=types["N"][1 - i].name, type="nominal"),  # type: ignore
                    )
                    children.append(child)

            # Grouped Bar
            for i in range(2):
                for agg in ["count", "sum", "mean", "max", "min"]:
                    child = deepcopy(self)
                    child.aggregation = Aggregation(
                        by=[types["N"][0].name, types["N"][1].name], type=agg
                    )
                    child.encoding = Encodings(
                        "grouped_bar",
                        alt.X(field=types["N"][i].name, type="nominal"),  # type: ignore
                        alt.Y(field=types["Q"][0].name, type="quantitative", aggregate=agg),  # type: ignore
                        alt.Column(field=types["N"][1 - i].name, type="nominal"),  # type: ignore
                    )
                    children.append(child)

            # Heatmap
            for agg in ["mean", "max"]:
                child = deepcopy(self)
                child.encoding = Encodings(
                    "rect",
                    alt.X(field=types["N"][0].name, type="nominal"),  # type: ignore
                    alt.Y(field=types["N"][1].name, type="nominal"),  # type: ignore
                    alt.Color(field=types["Q"][0].name, type="quantitative", aggregate=agg),  # type: ignore
                )
                children.append(child)

        return children

    def get_chart(self) -> alt.Chart:
        chart = alt.Chart(self.sub_df)  # type: ignore

        if self.encoding is None:
            return chart

        chart: alt.Chart = chart.encode(x=self.encoding.x, y=self.encoding.y)

        if self.encoding.chart_type == "circle":
            chart = chart.mark_circle()
            if self.encoding.z:
                chart = chart.encode(color=self.encoding.z)
        elif self.encoding.chart_type == "bar":
            chart = chart.mark_bar()
        elif self.encoding.chart_type == "grouped_bar":
            chart = chart.mark_bar().encode(column=self.encoding.z)
        elif self.encoding.chart_type == "stacked_bar":
            chart = chart.mark_bar().encode(color=self.encoding.z)
        elif self.encoding.chart_type == "rect":
            chart = chart.mark_rect().encode(color=self.encoding.z)
        elif self.encoding.chart_type == "line":
            chart = chart.mark_line()
        elif self.encoding.chart_type == "area":
            chart = chart.mark_area()
        elif self.encoding.chart_type == "arc":
            chart = alt.Chart(self.sub_df)  # type: ignore
            chart = chart.mark_arc()
            chart = chart.encode(
                color=self.encoding.x,
                theta=self.encoding.y,
            )
        return chart

    def get_number_of_types(
        self,
    ) -> dict[Literal["Q", "N", "T", "O"], list["Attribute"]]:
        types: dict[Literal["Q", "N", "T", "O"], list["Attribute"]] = {
            "Q": [],
            "N": [],
            "O": [],
            "T": [],
        }
        for attr in self.attrs:
            if self.sub_df[attr.name].nunique() != 1:
                types[attr.type].append(attr)
        return types

    def get_bov(self) -> Set[str]:
        bov: Set[str] = set()
        bov.update([f"attr_{attr.name}" for attr in self.attrs])
        if self.filters:
            bov.update([f"filter_to_{filter[0]}" for filter in self.filters])
            bov.update([f"filter_by_{filter[2]}" for filter in self.filters])
        if self.binnings:
            bov.update([f"bin_by_{binning.by}" for binning in self.binnings])
        if self.aggregation:
            bov.add(f"agg_by_{self.aggregation.by}")
            bov.add(f"agg_type_{self.aggregation.type}")
        if self.encoding:
            bov.add(self.encoding.chart_type)
        return bov

    def get_coverage(self, raw_df: pd.DataFrame) -> dict[str, float]:
        row_ratio = len(self.sub_df) / len(raw_df)
        coverage = {attr.name: 1.0 * row_ratio for attr in self.attrs}
        if self.binnings:
            for binning in self.binnings:
                coverage[binning.by] *= 0.75
        if self.aggregation:
            for attr in self.aggregation.by:
                coverage[attr] *= 0.5
        return coverage

    def get_info(self) -> str:
        info = ""
        info += f"Attributes: {[attr.name for attr in self.attrs]}\n"
        if self.filters:
            info += f"Filters: {[[f[0], f[1]]  for f in self.filters]}\n"
        if self.binnings:
            info += f"Binnings: {[binning.by for binning in self.binnings]}\n"
        if self.aggregation:
            info += f"Aggregation: {self.aggregation.type}({self.aggregation.by})\n"
        if self.encoding:
            info += f"Encodings: {self.encoding}\n"
        return info
