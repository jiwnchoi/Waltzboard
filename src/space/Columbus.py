import pandas as pd
from itertools import combinations
from typing import TYPE_CHECKING, Literal
from config import MAX_TARGET_ATTRIBUTES, AggregationType, FILTER_VALUE_THRESHOLD


from .DataModel import Attribute
from .DataTransforms import (
    apply_aggregation,
    apply_binning,
    apply_filtering,
    apply_sorting,
)
from .Node import VISNode
from .Encodings import encode_node


agg_types: list[AggregationType] = ["max", "min", "mean", "sum"]


class Columbus:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.types: list[Literal["Q", "N", "T", "O"]] = [
            "N" if df[col].dtype == "object" else "Q" for col in df.columns
        ]
        self.attrs: list["Attribute"] = [
            Attribute(str(name), type, False)
            for name, type in zip(df.columns, self.types)
        ]
        self.queue: list["VISNode"] = []
        self.nodes: list["VISNode"] = []
        # get {(n + 2) (n + 1) n / 6} combinations of attributes
        for i in range(1, MAX_TARGET_ATTRIBUTES + 1):
            for comb in combinations(self.attrs, i):
                self.queue.append(VISNode(list(comb), df))

        print(len(self.queue))

        while len(self.queue) > 0:
            node = self.queue.pop()

            visualizable_node = encode_node(node)

            if len(visualizable_node.encodings) > 0:
                self.nodes.append(visualizable_node)

            if not node.is_transformable():
                continue

            num_types = node.get_number_of_types()

            # Can count
            if num_types["Q"] == 0 and True not in set(
                [attr.immutable for attr in node.attrs]
            ):
                new_node = apply_aggregation(
                    node, [attr.name for attr in node.attrs], "count"
                )
                self.queue.append(new_node)

            for attr in node.attrs:
                if len(node.attrs) < 4:
                    # Can aggregate
                    if (
                        (attr.type == "N" or attr.type == "O")
                        and attr.immutable == False
                        and (num_types["N"] == 1 or num_types["O"] == 1)
                        and num_types["Q"] == len(node.attrs) - 1
                    ):
                        for agg_type in agg_types:
                            new_node = apply_aggregation(node, [attr.name], agg_type)
                            self.queue.append(new_node)
                    # Can bin
                    if attr.type == "Q" and attr.immutable == False:
                        new_node = apply_binning(node, attr.name)
                        self.queue.append(new_node)

                # Can filter
                if attr.type == "N" and attr.immutable == False:
                    unique_value = node.raw_df[attr.name].unique().tolist()
                    if len(unique_value) < FILTER_VALUE_THRESHOLD:
                        for value in unique_value:
                            if value == None:
                                continue
                            new_node = apply_filtering(node, attr.name, value, "eq")
                            self.queue.append(new_node)

    def get_nodes(self) -> list["VISNode"]:
        return self.nodes

    def get_visualizations(self) -> list["VISNode"]:
        return [node for node in self.nodes if len(node.encodings) > 0]
