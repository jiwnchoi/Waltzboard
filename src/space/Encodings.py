from typing import TYPE_CHECKING

from .DataTransforms import apply_aggregation, apply_binning
from .EncodingsModel import *

from config import MAX_UNIQUE_CATEGORY, MAX_UNIQUE_AXIS

if TYPE_CHECKING:
    from .Node import VISNode


# 2D Encoding


def encode_node(node: "VISNode") -> "VISNode":
    attr_types = node.get_number_of_types()
    node = node.get_copy()
    df = node.get_df()
    if df is None:
        return node
    row, _ = df.shape

    if node.dim == 1:
        if (
            node.attrs[0].type == "N"
            and df[node.attrs[0].name].nunique() < MAX_UNIQUE_CATEGORY + 1
        ):
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
        elif (
            len(attr_types["Q"]) == 1
            and len(attr_types["N"]) == 1
            and df[node.attrs[attr_types["N"][0]].name].nunique() < MAX_UNIQUE_AXIS + 1
        ):
            node.encodings = [
                SingleBar(
                    node.attrs[attr_types["N"][0]], node.attrs[attr_types["Q"][0]]
                ),
            ]

        # OQ -> Line, Bar
        elif len(attr_types["O"]) == 1 and len(attr_types["Q"]) == 1:
            node.encodings = [
                # SingleLine(
                #     node.attrs[attr_types["O"][0]], node.attrs[attr_types["Q"][0]]
                # ),
                SingleBar(
                    node.attrs[attr_types["O"][0]], node.attrs[attr_types["Q"][0]]
                ),
            ]

        # NN -> Heatmap
        elif (
            len(attr_types["N"]) == 2
            and df[node.attrs[0].name].nunique() < MAX_UNIQUE_AXIS + 1
            and df[node.attrs[1].name].nunique() < MAX_UNIQUE_AXIS + 1
        ):
            node = apply_aggregation(node, [attr.name for attr in node.attrs], "count")
            df = node.get_df()
            if isinstance(df, pd.DataFrame) and df["count"].nunique() > 3:
                node.encodings = [
                    Heatmap(node.attrs[0], node.attrs[1], node.attrs[2]),
                ]
            else:
                node.encodings = []

        # ON -> Heatmap
        elif (
            len(attr_types["O"]) == 1
            and len(attr_types["N"]) == 1
            and df[node.attrs[attr_types["N"][0]].name].nunique() < MAX_UNIQUE_AXIS + 1
        ):
            node = apply_aggregation(node, [attr.name for attr in node.attrs], "count")
            df = node.get_df()
            if isinstance(df, pd.DataFrame) and df["count"].nunique() > 3:
                node.encodings = [
                    Heatmap(
                        node.attrs[attr_types["O"][0]],
                        node.attrs[attr_types["N"][0]],
                        node.attrs[2],
                    ),
                ]
            else:
                node.encodings = []

        # OO -> Heatmap
        elif len(attr_types["O"]) == 2:
            node = apply_aggregation(node, [attr.name for attr in node.attrs], "count")
            df = node.get_df()
            if isinstance(df, pd.DataFrame) and df["count"].nunique() > 3:
                node.encodings = [
                    Heatmap(node.attrs[0], node.attrs[1], node.attrs[2]),
                ]
            else:
                node.encodings = []

    elif node.dim == 3:
        # Q2 N1
        if (
            len(attr_types["Q"]) == 2
            and len(attr_types["N"]) == 1
            and 1 < df[node.attrs[attr_types["N"][0]].name].nunique()
            < MAX_UNIQUE_CATEGORY + 1
        ):
            node.encodings = [
                ColoredScatter(
                    x=node.attrs[attr_types["Q"][0]],
                    y=node.attrs[attr_types["Q"][1]],
                    color=node.attrs[attr_types["N"][0]],
                ),
            ]

        # Q1 N2
        elif (
            len(attr_types["Q"]) == 1
            and len(attr_types["N"]) == 2
            and 1 < df[node.attrs[attr_types["N"][0]].name].nunique()
            < MAX_UNIQUE_CATEGORY + 1
            and 1 < df[node.attrs[attr_types["N"][1]].name].nunique() < MAX_UNIQUE_AXIS + 1
        ):
            node.encodings = [
                GroupedBar(
                    group=node.attrs[attr_types["N"][0]],
                    x=node.attrs[attr_types["N"][1]],
                    y=node.attrs[attr_types["Q"][0]],
                ),
                StackedBar(
                    x=node.attrs[attr_types["N"][1]],
                    y=node.attrs[attr_types["Q"][0]],
                    color=node.attrs[attr_types["N"][0]],
                ),
            ]

        elif (
            len(attr_types["Q"]) == 1
            and len(attr_types["N"]) == 2
            and 1
            < df[node.attrs[attr_types["N"][1]].name].nunique()
            < MAX_UNIQUE_CATEGORY + 1
            and df[node.attrs[attr_types["N"][0]].name].nunique() < MAX_UNIQUE_AXIS + 1
        ):
            node.encodings = [
                GroupedBar(
                    group=node.attrs[attr_types["N"][1]],
                    x=node.attrs[attr_types["N"][0]],
                    y=node.attrs[attr_types["Q"][0]],
                ),
                StackedBar(
                    x=node.attrs[attr_types["N"][0]],
                    y=node.attrs[attr_types["Q"][0]],
                    color=node.attrs[attr_types["N"][1]],
                ),
            ]

        elif (
            len(attr_types["Q"]) == 1
            and len(attr_types["N"]) == 2
            and 1 < df[node.attrs[attr_types["N"][0]].name].nunique() < MAX_UNIQUE_AXIS + 1
            and 1 < df[node.attrs[attr_types["N"][1]].name].nunique() < MAX_UNIQUE_AXIS + 1
            and df[node.attrs[attr_types["Q"][0]].name].nunique() > 3
        ):
            node.encodings = [
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
