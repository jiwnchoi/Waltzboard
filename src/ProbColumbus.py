# type: ignore
from numpy.random import choice
from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from math import ceil
from os import cpu_count
from typing import Literal, Any, TypeVar
import altair as alt
import pandas as pd
from pathos.multiprocessing import ProcessingPool as Pool
import numpy as np

from .oracle import ColumbusOracle, OracleResult, OracleWeight, ColumbusProbOracle
from .oracle.Interestingness import get_statistic_feature_hashmap
from .space.DataModel import Attribute, VisualizableDataFrame
from .space.Node import VisualizationNode
from .space.ProbabilisticNode import ProbabilisticNode
from .ChartMap import chart_map
import altair as alt


@dataclass
class ColumbusConfig:
    max_attributes: int = 3
    max_categories: int = 10
    max_filters: int = 1
    min_rows: int = 4

    def to_dict(self):
        return {
            "max_attributes": self.max_attributes,
            "max_categories": self.max_categories,
            "max_filters": self.max_filters,
            "min_rows": self.min_rows,
        }


chart_type = ["bar", "point", "arc", "rect", "tick", "boxplot"]
agg_type = [None, "mean", "max", "sum", "min", "count"]


def histogram(label: list[str], x: np.ndarray) -> alt.Chart:
    return (
        alt.Chart(pd.DataFrame({"x": x, "label": label}))
        .mark_bar()
        .encode(y="x:Q", x="label:N")
        .properties(width=100)
    )


@dataclass
class SamplingWeight:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    ct: np.ndarray
    at: np.ndarray
    attr: list
    chart_type: list[str]
    agg_type: list[str]

    def visualize(self):
        return alt.hconcat(
            histogram(self.attr[1:], self.x),
            histogram(self.attr, self.y),
            histogram(self.attr, self.z),
            histogram(self.chart_type, self.ct),
            histogram(self.agg_type, self.at),
        )


T = TypeVar("T")


def is_valid_map(current: list, map: list) -> bool:
    return all(
        [
            map[i] == c.type if isinstance(c, Attribute) else map[i] == c
            for i, c in enumerate(current)
        ]
    )


class ProbColumbus:
    def __init__(self, df: pd.DataFrame, config: ColumbusConfig) -> None:
        self.df = df
        self.attrs = np.array(
            [None]
            + [
                Attribute(col, "C" if df[col].dtype == "object" else "Q")
                for col in df.columns
            ]
        )
        self.dic = {
            col: Attribute(col, "C" if df[col].dtype == "object" else "Q")
            for col in df.columns
        }
        self.dic[None] = None

    def attr_filtered_weight(
        self, current: list["Attribute"], weight: np.ndarray
    ) -> np.ndarray:
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map if e is not None])
        weight_mask = np.array(
            [True] + [e.type in valid_type and e not in current for e in self.attrs[1:]]
        )
        return weight * weight_mask

    def ct_filtered_weight(self, current: list, weight: np.ndarray) -> np.ndarray:
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in chart_type])
        return weight * weight_mask

    def at_filtered_weight(self, current: list, weight: np.ndarray) -> np.ndarray:
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in agg_type])
        return weight * weight_mask

    def _sample_one(self, weight: SamplingWeight):
        current = []
        x = choice(self.attrs[1:], p=weight.x / weight.x.sum())
        current.append(x)
        weight_y = self.attr_filtered_weight(current, weight.y)
        y = choice(self.attrs, p=weight_y / weight_y.sum())
        current.append(y)

        if y:
            weight_z = self.attr_filtered_weight(current, weight.z)
            z = choice(self.attrs, p=weight_z / weight_z.sum())
            current.append(z)
        else:
            z = None
            current.append(z)
        weight_ct = self.ct_filtered_weight(current, weight.ct)
        ct = choice(chart_type, p=weight_ct / weight_ct.sum())
        current.append(ct)
        weight_at = self.at_filtered_weight(current, weight.at)
        at = choice(agg_type, p=weight_at / weight_at.sum())
        current.append(at)
        return current

    # not using choice, select the max weight one
    def _sample_max(self, weight: SamplingWeight):
        current = []
        x = self.attrs[1:][np.argmax(weight.x)]
        current.append(x)
        weight_y = self.attr_filtered_weight(current, weight.y)
        y = self.attrs[np.argmax(weight_y)]
        current.append(y)

        if y:
            weight_z = self.attr_filtered_weight(current, weight.z)
            z = self.attrs[np.argmax(weight_z)]
            current.append(z)
        else:
            z = None
            current.append(z)
        weight_ct = self.ct_filtered_weight(current, weight.ct)
        ct = chart_type[np.argmax(weight_ct)]
        current.append(ct)
        weight_at = self.at_filtered_weight(current, weight.at)
        at = agg_type[np.argmax(weight_at)]
        current.append(at)
        return current

    def sample_one(self, weight: SamplingWeight):
        sample = []
        while len(sample) == 0:
            sample.append(self._sample_one(weight))

        return ProbabilisticNode(sample[0], self.df)

    def sample_max_one(self, weight: SamplingWeight):
        sample = []
        while len(sample) == 0:
            sample.append(self._sample_max(weight))
        return ProbabilisticNode(sample[0], self.df)

    def sample_n(self, n: int, weight) -> list[ProbabilisticNode]:
        return [self.sample_one(weight) for _ in range(n)]

    def sample_max_n(self, n: int, weight) -> list[ProbabilisticNode]:
        return [self.sample_max_one(weight) for _ in range(n)]

    def get_node(self, sample: list) -> ProbabilisticNode:
        new_sample = [self.dic[key] for key in sample[:3]] + sample[3:]
        return ProbabilisticNode(new_sample, self.df)

    def infer(
        self,
        nodes: list[ProbabilisticNode],
        oracle: ColumbusProbOracle,
        wildcard: list[str],
    ):
        result = oracle.get_result(nodes, self.df, set(wildcard))
        return float(result.get_score())
