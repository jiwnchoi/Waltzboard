# type: ignore

from typing import Literal, Optional, Set, Union
import altair as alt
import pandas as pd
import json

from . import (
    Aggregation,
    Binning,
    Encodings,
    Attribute,
)


class GleanerChart:
    sample: list[Union["Attribute", str, None]]
    index: Optional[int]
    sub_df: pd.DataFrame
    attrs: list["Attribute"]

    filters: Optional[list[tuple[str, str, str]]] = None
    binnings: Optional[list["Binning"]] = None
    aggregation: Optional["Aggregation"] = None
    chart_type: str = None
    encoding: Optional["Encodings"] = None

    def __init__(self, result: list, df: pd.DataFrame) -> None:
        chart_type, x, y, z, agg_type = result
        self.attrs = [x, y, z] if z else [x, y] if y else [x]
        self.sample = result
        for i in range(len(self.attrs)):
            self.sample[i + 1] = self.attrs[i].name

        self.sub_df = df[
            [x.name, y.name, z.name] if z else [x.name, y.name] if y else [x.name]
        ]
        self.chart_type = chart_type

        dim = len(self.attrs)

        if dim == 1 and x.type == "Q" and agg_type:
            self.binnings = [Binning(x.name, x.type)]
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type(), bin=True),
                y=alt.Y(x.name, type=x.long_type(), aggregate=agg_type),
            )

        elif dim == 1 and x.type == "Q":
            self.encoding = Encodings(
                chart_type=chart_type, x=alt.X(x.name, type=x.long_type())
            )

        elif dim == 1 and x.type == "C" and chart_type == "arc":
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.Color(x.name, type=x.long_type()),
                y=alt.Theta(x.name, aggregate=agg_type),
            )

        elif dim == 1 and x.type == "C":
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(x.name, aggregate="count"),
            )

        elif dim == 2 and x.type == "Q" and y.type == "Q" and agg_type:
            self.aggregation = Aggregation([x.name, y.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type(), bin=True),
                y=alt.Y(y.name, type=y.long_type(), bin=True),
                z=alt.Color(aggregate=agg_type),
            )

        elif dim == 2 and x.type == "Q" and y.type == "Q":
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type()),
            )

        elif (
            dim == 2
            and x.type == "C"
            and y.type == "Q"
            and chart_type == "bar"
            and agg_type == "count"
        ):
            self.binnings = [Binning(x.name)]
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type(), bin=True),
                y=alt.Y(x.name, type=x.long_type(), aggregate=agg_type),
                z=alt.Color(y.name, type=y.long_type()),
            )

        elif dim == 2 and x.type == "C" and y.type == "Q" and chart_type == "bar":
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type(), aggregate=agg_type),
            )

        elif dim == 2 and x.type == "C" and y.type == "Q" and chart_type == "arc":
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.Color(x.name, type=x.long_type()),
                y=alt.Theta(y.name, type=y.long_type(), aggregate=agg_type),
            )

        elif dim == 2 and x.type == "C" and y.type == "Q":
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type()),
            )

        elif dim == 2 and x.type == "Q" and y.type == "C":
            self.binnings = [Binning(x.name)]
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type(), bin=True),
                y=alt.Y(x.name, type=x.long_type(), aggregate=agg_type),
                z=alt.Color(y.name, type=y.long_type()),
            )

        elif dim == 2 and x.type == "C" and y.type == "C":
            self.aggregation = Aggregation([x.name, y.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type()),
                z=alt.Color(aggregate=agg_type),
            )

        elif (
            dim == 3
            and x.type == "Q"
            and y.type == "Q"
            and z.type == "Q"
            and chart_type == "point"
        ):
            self.binnings = [Binning(z.name)]
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type()),
                z=alt.Color(z.name, type=z.long_type(), bin=True),
            )

        elif (
            dim == 3
            and x.type == "Q"
            and y.type == "Q"
            and z.type == "Q"
            and chart_type == "rect"
        ):
            self.binnings = [Binning(x.name), Binning(y.name)]
            self.aggregation = Aggregation([x.name, y.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type(), bin=True),
                y=alt.Y(y.name, type=y.long_type(), bin=True),
                z=alt.Color(z.name, type=z.long_type(), aggregate=agg_type),
            )

        elif dim == 3 and x.type == "Q" and y.type == "Q" and z.type == "C":
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type()),
                z=alt.Color(z.name, type=z.long_type()),
            )

        # qcq rect agg
        elif dim == 3 and x.type == "Q" and y.type == "C" and z.type == "Q":
            self.aggregation = Aggregation([x.name, y.name], agg_type)
            self.binnings = [Binning(x.name)]
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type(), bin=True),
                y=alt.Y(y.name, type=y.long_type()),
                z=alt.Color(z.name, type=z.long_type(), aggregate=agg_type),
            )

        # cqc bar sum
        elif dim == 3 and x.type == "C" and y.type == "Q" and z.type == "C":
            self.aggregation = Aggregation([x.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type(), aggregate=agg_type),
                z=alt.Color(z.name, type=z.long_type()),
            )

        # ccq react mean
        elif dim == 3 and x.type == "C" and y.type == "C" and z.type == "Q":
            self.aggregation = Aggregation([x.name, y.name], agg_type)
            self.encoding = Encodings(
                chart_type=chart_type,
                x=alt.X(x.name, type=x.long_type()),
                y=alt.Y(y.name, type=y.long_type()),
                z=alt.Color(z.name, type=z.long_type(), aggregate=agg_type),
            )

    def get_vegalite(self) -> alt.VegaLiteSchema:
        chart = self.display()
        chart.configure_legend(title=None)
        return chart.to_json()

    def display(self) -> alt.Chart:
        num_fields = len(self.attrs)
        axis_names = [attr.name for attr in self.attrs]
        value_field_name = axis_names[-1]

        filter_tokens = (
            [
                ["and" if i > 0 else "", f[0], "is", f[1]]
                for i, f in enumerate(self.filters)
            ]
            if self.filters
            else [],
        )

        tokens: list[str] = [
            [f"{self.aggregation.type[0].upper()}{self.aggregation.type[1:]}", "of"]
            if self.aggregation
            else [],
            [value_field_name],
            ["of"] if self.aggregation else [],
            ["by", axis_names[0], "and", axis_names[1]] if num_fields == 3 else [],
            ["by", axis_names[0]] if num_fields == 2 else [],
            [",", "when", *filter_tokens] if self.filters else [],
        ]
        tokens = [t for token in tokens for t in token]

        chart = alt.Chart(self.sub_df, title=" ".join(tokens)).properties(
            description=json.dumps(tokens)
        )
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

        # Swap x and y axis for better readability
        if (
            num_fields > 2
            and self.encoding.x.type == "nominal"
            and self.encoding.y.type == "nominal"
        ):
            x_max_char = max(
                [len(x) for x in self.sub_df[axis_names[0]].dropna().unique().tolist()]
            )
            y_max_char = max(
                [len(y) for y in self.sub_df[axis_names[1]].dropna().unique().tolist()]
            )
            if x_max_char > y_max_char:
                chart = chart.encode(y=self.encoding.x, x=self.encoding.y)

        elif (
            num_fields > 1
            and self.encoding.x.type == "nominal"
            and self.encoding.chart_type != "arc"
        ):
            chart = chart.encode(x=self.encoding.y, y=self.encoding.x)

        elif (
            num_fields == 1
            and self.encoding.x.type == "nominal"
            and self.encoding.chart_type != "arc"
        ):
            chart = chart.encode(x=None, y=self.encoding.x)

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
        bov.update([f"{attr.name}" for attr in self.attrs])
        if self.filters:
            bov.update([f"filter_to_{filter[0]}" for filter in self.filters])
            bov.update([f"filter_by_{filter[2]}" for filter in self.filters])
        if self.binnings:
            bov.update([f"bin_by_{binning.by}" for binning in self.binnings])
        if self.aggregation:
            bov.add(f"agg_by_{self.aggregation.by}")
            bov.add(f"{self.aggregation.type}")
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
