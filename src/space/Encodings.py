from dataclasses import dataclass
from typing import Union, TYPE_CHECKING

from . import Attribute, apply_aggregation, apply_binning
import altair as alt

if TYPE_CHECKING:
    from . import VISNode


# 2D Encoding
@dataclass
class SingleBar:
    x: Attribute
    y: Attribute

    def __str__(self) -> str:
        return f"SingleBar({self.x.name}, {self.y.name})"


@dataclass
class SingleLine:
    x: Attribute
    y: Attribute

    def __str__(self) -> str:
        return f"SingleLine({self.x.name}, {self.y.name})"


@dataclass
class Scatter:
    x: Attribute
    y: Attribute

    def __str__(self) -> str:
        return f"Scatter({self.x.name}, {self.y.name})"


@dataclass
class Pie:
    color: Attribute
    theta: Attribute

    def __str__(self) -> str:
        return f"Pie({self.color.name}, {self.theta.name})"


# 3D Encoding
@dataclass
class Heatmap:
    x: Attribute
    y: Attribute
    color: Attribute

    def __str__(self) -> str:
        return f"Heatmap({self.x.name}, {self.y.name}, {self.color.name})"


@dataclass
class GroupedBar:
    x: Attribute
    y: Attribute
    group: Attribute

    def __str__(self) -> str:
        return f"GroupedBar({self.x.name}, {self.y.name}, {self.group.name})"


@dataclass
class StackedBar:
    x: Attribute
    y: Attribute
    color: Attribute

    def __str__(self) -> str:
        return f"StackedBar({self.x.name}, {self.y.name}, {self.color.name})"


@dataclass
class ColoredScatter:
    x: Attribute
    y: Attribute
    color: Attribute

    def __str__(self) -> str:
        return f"ColoredScatter({self.x.name}, {self.y.name}, {self.color.name})"


@dataclass
class MultiLine:
    x: Attribute
    y: Attribute
    color: Attribute

    def __str__(self) -> str:
        return f"MultiLine({self.x.name}, {self.y.name}, {self.color.name})"


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


def get_encoded_node(node: "VISNode") -> "VISNode":
    attr_types = node.get_number_of_types()
    node = node.get_copy()
    if node.dim == 1:
        if node.attrs[0].type == "N":
            node = apply_aggregation(node, [node.attrs[0].name], "count")
            node.encodings = [
                SingleBar(node.attrs[0], node.attrs[1]),
                Pie(node.attrs[0], node.attrs[1]),
            ]

        elif node.attrs[0].type == "Q":
            node = apply_binning(node, node.attrs[0].name)
            node = apply_aggregation(node, [node.attrs[0].name], "count")
            node.encodings = [
                SingleBar(node.attrs[0], node.attrs[1]),
            ]

    elif node.dim == 2:
        # QQ -> Scatter
        if len(attr_types["Q"]) == 2:
            node.encodings = [
                Scatter(node.attrs[0], node.attrs[1]),
            ]

        # QN -> Bar
        if len(attr_types["Q"]) == 1 and len(attr_types["N"]) == 1:
            node.encodings = [
                SingleBar(
                    node.attrs[attr_types["N"][0]], node.attrs[attr_types["Q"][0]]
                ),
            ]

        # OQ -> Line, Bar
        if len(attr_types["O"]) == 1 and len(attr_types["Q"]) == 1:
            node.encodings = [
                SingleLine(
                    node.attrs[attr_types["O"][0]], node.attrs[attr_types["Q"][0]]
                ),
                SingleBar(
                    node.attrs[attr_types["O"][0]], node.attrs[attr_types["Q"][0]]
                ),
            ]

        # NN -> Heatmap
        if len(attr_types["N"]) == 2:
            node = apply_aggregation(node, [attr.name for attr in node.attrs], "count")
            node.encodings = [
                Heatmap(node.attrs[0], node.attrs[1], node.attrs[2]),
            ]

        # ON -> Heatmap
        if len(attr_types["O"]) == 1 and len(attr_types["N"]) == 1:
            node = apply_aggregation(node, [attr.name for attr in node.attrs], "count")
            node.encodings = [
                Heatmap(
                    node.attrs[attr_types["O"][0]],
                    node.attrs[attr_types["N"][0]],
                    node.attrs[2],
                ),
            ]

        # OO -> Heatmap
        if len(attr_types["O"]) == 2:
            node = apply_aggregation(node, [attr.name for attr in node.attrs], "count")
            node.encodings = [
                Heatmap(node.attrs[0], node.attrs[1], node.attrs[2]),
            ]

    elif node.dim == 3:
        # Q2 N1
        if len(attr_types["Q"]) == 2 and len(attr_types["N"]) == 1:
            node.encodings = [
                ColoredScatter(
                    x=node.attrs[attr_types["Q"][0]],
                    y=node.attrs[attr_types["Q"][1]],
                    color=node.attrs[attr_types["N"][0]],
                ),
            ]

        # Q1 N2
        if len(attr_types["Q"]) == 1 and len(attr_types["N"]) == 2:
            node.encodings = [
                GroupedBar(
                    group=node.attrs[attr_types["N"][1]],
                    x=node.attrs[attr_types["N"][0]],
                    y=node.attrs[attr_types["Q"][0]],
                ),
                GroupedBar(
                    group=node.attrs[attr_types["N"][0]],
                    x=node.attrs[attr_types["N"][1]],
                    y=node.attrs[attr_types["Q"][0]],
                ),
                StackedBar(
                    x=node.attrs[attr_types["N"][0]],
                    y=node.attrs[attr_types["Q"][0]],
                    color=node.attrs[attr_types["N"][1]],
                ),
                StackedBar(
                    x=node.attrs[attr_types["N"][1]],
                    y=node.attrs[attr_types["Q"][0]],
                    color=node.attrs[attr_types["N"][0]],
                ),
                Heatmap(
                    x=node.attrs[attr_types["N"][0]],
                    y=node.attrs[attr_types["N"][1]],
                    color=node.attrs[attr_types["Q"][0]],
                ),
            ]

        # Q3
        if attr_types["Q"] == 3:
            pass

    return node
