# type: ignore
from dataclasses import dataclass
from typing import TypeVar

import altair as alt
import numpy as np
import pandas as pd
from numpy.random import dirichlet, choice


from ..ChartMap import chart_map
from ..model.DataModel import Attribute
from ..model.Node import VisualizationNode
from ..ChartMap import chart_type, agg_type


@dataclass
class SamplingWeight:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    ct: np.ndarray
    at: np.ndarray
    n_chart: float


def is_valid_map(current: list, map: list) -> bool:
    return all(
        [
            map[i] == c.type if isinstance(c, Attribute) else map[i] == c
            for i, c in enumerate(current)
        ]
    )


class Explorer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.attrs: list[None | Attribute] = [None] + [
            Attribute(col, "C" if df[col].dtype == "object" else "Q")
            for col in df.columns
        ]

    def attr_mask(self, current: list["Attribute"]):
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array(
            [
                (e is None and e in valid_type)
                or (
                    isinstance(e, Attribute)
                    and e.type in valid_type
                    and e not in current
                )
                for e in self.attrs
            ]
        )
        return weight_mask

    def ct_mask(self, current: list):
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in chart_type])
        return weight_mask

    def at_mask(self, current: list):
        valid_map = [e for e in chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in agg_type])
        return weight_mask

    def sample_one(self, weight: SamplingWeight) -> VisualizationNode:
        current: list = []

        mask_ct = self.ct_mask(current)
        current.append(choice(chart_type, p=p(dirichlet(weight.ct) * mask_ct)))

        mask_x = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(dirichlet(weight.x) * mask_x)))

        mask_y = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(dirichlet(weight.y) * mask_y)))

        mask_z = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(dirichlet(weight.z) * mask_z)))

        mask_at = self.at_mask(current)
        current.append(choice(agg_type, p=p(dirichlet(weight.at) * mask_at)))

        return VisualizationNode(current, self.df)

    def sample_n(self, n: int, weight) -> list[VisualizationNode]:
        return [self.sample_one(weight) for _ in range(n)]


def p(x: np.ndarray) -> np.ndarray:
    return x / x.sum()
