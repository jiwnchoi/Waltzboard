# type: ignore

from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Optional, Set, Union

import altair as alt
import pandas as pd

from .DataTransformsModel import Aggregation, Binning

if TYPE_CHECKING:
    from .DataModel import Attribute


chart_type = Literal["bar", "line", "point", "area", "arc", "rect", "tick", "boxplot"]


@dataclass
class Encodings:
    chart_type: str
    x: Union[alt.X, alt.Color]
    y: Union[alt.Y, alt.Theta, None] = None
    z: Union[alt.Color, alt.Column, alt.Y, None] = None


@dataclass
class VisualizationNode:
    sub_df: pd.DataFrame
    attrs: list["Attribute"]

    filters: Optional[list[tuple[str, str, str]]]
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

        if dim == 1 and filtered_attrs[0].type == "C":
            for encoding in ["bar", "arc"]:
                child = deepcopy(self)
                child.aggregation = Aggregation(by=[types["C"][0].name], type="count")
                child.encoding = Encodings(
                    encoding,
                    alt.X(field=types["C"][0].name, type="nominal"),
                    alt.Y(field=types["C"][0].name, aggregate="count", type="nominal"),
                )
                children.append(child)

        elif dim == 1 and filtered_attrs[0].type == "Q":
            # Stripplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "tick", x=alt.X(field=types["Q"][0].name, type="quantitative")
            )
            children.append(child)

            # Histogram
            child = deepcopy(self)
            child.binnings = [Binning(by=types["Q"][0].name)]
            child.aggregation = Aggregation(by=[types["Q"][0].name], type="count")
            child.encoding = Encodings(
                "bar",
                alt.X(field=types["Q"][0].name, type="quantitative", bin=True),
                alt.Y(field=types["Q"][0].name, aggregate="count", type="quantitative"),
            )
            children.append(child)

        # QQ
        elif dim == 2 and len(types["Q"]) == 2:
            # Scatterplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "point",
                alt.X(field=types["Q"][0].name, type="quantitative"),
                alt.Y(field=types["Q"][1].name, type="quantitative"),
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
                alt.X(field=types["Q"][0].name, type="quantitative", bin=True),
                alt.Y(field=types["Q"][1].name, type="quantitative", bin=True),
                alt.Color(aggregate="count", type="quantitative"),
            )
            children.append(child)

        # QN
        elif dim == 2 and len(types["Q"]) == 1 and len(types["C"]) == 1:
            # Bar
            for agg in ["sum", "mean", "max", "min"]:
                child = deepcopy(self)
                child.aggregation = Aggregation(by=[types["C"][0].name], type=agg)
                child.encoding = Encodings(
                    "bar",
                    alt.X(field=types["C"][0].name, type="nominal"),
                    alt.Y(field=types["Q"][0].name, type="quantitative", aggregate=agg),
                )
                children.append(child)

            # Pie
            for agg in ["sum", "mean", "max", "min"]:
                child = deepcopy(self)
                child.aggregation = Aggregation(by=[types["C"][0].name], type=agg)
                child.encoding = Encodings(
                    "arc",
                    alt.Color(field=types["C"][0].name, type="nominal"),
                    alt.Theta(
                        field=types["Q"][0].name, type="quantitative", aggregate=agg
                    ),
                )
                children.append(child)

            # Stripplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "tick",
                alt.X(field=types["Q"][0].name, type="quantitative"),
                alt.Y(field=types["C"][0].name, type="nominal"),
            )
            children.append(child)

            # Boxplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "boxplot",
                alt.X(field=types["C"][0].name, type="nominal"),
                alt.Y(field=types["Q"][0].name, type="quantitative"),
            )
            children.append(child)

            # Layered Histogram
            child = deepcopy(self)
            child.binnings = [Binning(by=types["Q"][0].name)]
            child.aggregation = Aggregation(by=[types["Q"][0].name], type="count")
            child.encoding = Encodings(
                "bar",
                alt.X(field=types["Q"][0].name, type="quantitative", bin=True),
                alt.Y(field=types["Q"][0].name, aggregate=agg, type="quantitative"),
                alt.Color(field=types["C"][0].name, type="nominal"),
            )
            children.append(child)

        # NN
        elif dim == 2 and len(types["C"]) == 2:
            # Heatmap
            child = deepcopy(self)
            child.aggregation = Aggregation(
                by=[types["C"][0].name, types["C"][1].name], type="count"
            )
            child.encoding = Encodings(
                "rect",
                alt.X(field=types["C"][0].name, type="nominal"),
                alt.Y(field=types["C"][1].name, type="nominal"),
                alt.Color(aggregate="count", type="quantitative"),
            )
            children.append(child)

        # QQQ
        elif dim == 3 and len(types["Q"]) == 3:
            # Colored Scatterplot
            for i in range(3):
                child = deepcopy(self)
                child.binnings = [Binning(by=types["Q"][i].name)]
                child.encoding = Encodings(
                    "point",
                    alt.X(field=types["Q"][i].name, type="quantitative"),
                    alt.Y(field=types["Q"][(i + 1) % 3].name, type="quantitative"),
                    alt.Color(
                        field=types["Q"][(i + 2) % 3].name,
                        type="quantitative",
                        bin=True,
                    ),
                )
                children.append(child)

            # Heatmap
            for i in range(3):
                for agg in ["mean", "max"]:
                    child = deepcopy(self)
                    child.aggregation = Aggregation(
                        by=[types["Q"][i].name, types["Q"][(i + 1) % 3].name], type=agg
                    )
                    child.binnings = [
                        Binning(by=types["Q"][i].name),
                        Binning(by=types["Q"][(i + 1) % 3].name),
                    ]
                    child.encoding = Encodings(
                        "rect",
                        alt.X(field=types["Q"][i].name, type="quantitative", bin=True),
                        alt.Y(
                            field=types["Q"][(i + 1) % 3].name,
                            type="quantitative",
                            bin=True,
                        ),
                        alt.Color(
                            field=types["Q"][(i + 2) % 3].name,
                            type="quantitative",
                            aggregate=agg,
                        ),
                    )
                    children.append(child)

        # QQN
        elif dim == 3 and len(types["Q"]) == 2 and len(types["C"]) == 1:
            # Colored Scatterplot
            child = deepcopy(self)
            child.encoding = Encodings(
                "point",
                alt.X(field=types["Q"][0].name, type="quantitative"),
                alt.Y(field=types["Q"][1].name, type="quantitative"),
                alt.Color(field=types["C"][0].name, type="nominal"),
            )
            children.append(child)

            # Heatmap
            for i in range(2):
                for agg in ["mean", "max"]:
                    child = deepcopy(self)
                    child.binnings = [Binning(by=types["Q"][i].name)]
                    child.encoding = Encodings(
                        "rect",
                        alt.X(field=types["Q"][i].name, type="quantitative", bin=True),
                        alt.Y(field=types["C"][0].name, type="nominal"),
                        alt.Color(
                            field=types["Q"][1 - i].name,
                            type="quantitative",
                            aggregate=agg,
                        ),
                    )
                    children.append(child)

        # QNN
        elif dim == 3 and len(types["Q"]) == 1 and len(types["C"]) == 2:
            # Stacked Bar
            for i in range(2):
                for agg in ["count", "sum", "mean", "max", "min"]:
                    child = deepcopy(self)
                    child.aggregation = Aggregation(
                        by=[types["C"][0].name, types["C"][1].name], type=agg
                    )
                    child.encoding = Encodings(
                        "stacked_bar",
                        alt.X(field=types["C"][i].name, type="nominal"),
                        alt.Y(
                            field=types["Q"][0].name, type="quantitative", aggregate=agg
                        ),
                        alt.Color(field=types["C"][1 - i].name, type="nominal"),
                    )
                    children.append(child)

            # # Grouped Bar
            # for i in range(2):
            #     for agg in ["count", "sum", "mean", "max", "min"]:
            #         child = deepcopy(self)
            #         child.aggregation = Aggregation(
            #             by=[types["C"][0].name, types["C"][1].name], type=agg
            #         )
            #         child.encoding = Encodings(
            #             "grouped_bar",
            #             alt.X(field=types["C"][i].name, type="nominal"),
            #             alt.Y(
            #                 field=types["Q"][0].name, type="quantitative", aggregate=agg
            #             ),
            #             alt.Column(field=types["C"][1 - i].name, type="nominal"),
            #         )
            #         children.append(child)

            # Heatmap
            for agg in ["mean", "max"]:
                child = deepcopy(self)
                child.encoding = Encodings(
                    "rect",
                    alt.X(field=types["C"][0].name, type="nominal"),
                    alt.Y(field=types["C"][1].name, type="nominal"),
                    alt.Color(
                        field=types["Q"][0].name, type="quantitative", aggregate=agg
                    ),
                )
                children.append(child)

        return children

    def get_vegalite(self) -> alt.VegaLiteSchema:

        chart = self.get_altair()
        chart.configure_legend(title=None)
        return chart.to_json()

    def get_altair(self) -> alt.Chart:
        chart = alt.Chart(self.sub_df)

        if self.encoding is None:
            return chart

        chart: alt.Chart = chart.encode(x=self.encoding.x)
        if self.encoding.y:
            chart = chart.encode(y=self.encoding.y)

        if self.encoding.chart_type == "point":
            chart = chart.mark_point()
            if self.encoding.z:
                chart = chart.encode(color=self.encoding.z)
        elif self.encoding.chart_type == "bar":
            chart = chart.mark_bar()
        elif self.encoding.chart_type == "grouped_bar":
            chart = chart.mark_bar().encode(column=self.encoding.z)
        elif self.encoding.chart_type == "stacked_bar":
            chart = chart.mark_bar().encode(color=self.encoding.z)
        elif self.encoding.chart_type == "layered_bar":
            chart = chart.mark_bar().encode(color=self.encoding.z)
        elif self.encoding.chart_type == "rect":
            chart = chart.mark_rect().encode(color=self.encoding.z)
        elif self.encoding.chart_type == "line":
            chart = chart.mark_line()
        elif self.encoding.chart_type == "area":
            chart = chart.mark_area()
        elif self.encoding.chart_type == "arc":
            chart = alt.Chart(self.sub_df)
            chart = chart.mark_arc()
            chart = chart.encode(color=self.encoding.x, theta=self.encoding.y)
        elif self.encoding.chart_type == "boxplot":
            chart = chart.mark_boxplot(extent="min-max")
        elif self.encoding.chart_type == "tick":
            chart = chart.mark_tick()

        num_fields = (
            3
            if self.encoding.z
            else 2
            if self.encoding.y
            else 1
            if self.encoding.x
            else None
        )

        value_field_name = (
            self.encoding.z.field
            if num_fields == 3
            else self.encoding.y.field
            if num_fields == 2
            else self.encoding.x.field
            if num_fields == 1
            else None
        )

        desc = ""
        if self.aggregation:
            desc += f"{self.aggregation.type[0].upper()}{self.aggregation.type[1:]} of "
        desc += f"{value_field_name} "
        if num_fields == 3:
            desc += f"by {self.encoding.x.field} and {self.encoding.y.field} "
        elif num_fields == 2:
            desc += f"by {self.encoding.x.field}"
        if self.filters:
            desc += ", when "
            for i, f in enumerate(self.filters):
                if i > 0:
                    desc += " and "
                desc += f"{f[0]} is {f[1]}"

        chart = chart.properties(description=desc)

        return chart

    def get_number_of_types(
        self,
    ) -> dict[Literal["Q", "C", "T", "O", "N"], list["Attribute"]]:
        types: dict[Literal["Q", "C", "T", "O", "N"], list["Attribute"]] = {
            "Q": [],
            "C": [],
            "O": [],
            "T": [],
            "N": [],
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

