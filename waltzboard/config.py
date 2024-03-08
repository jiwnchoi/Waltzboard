from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

import pandas as pd

from waltzboard.model import (
    Attribute,
    ChartKeyTokens,
    ChartMap,
    ChartMapType,
    get_chart_from_tokens,
)
from waltzboard.oracle import OracleWeight

if TYPE_CHECKING:
    from waltzboard.model import BaseChart


class WaltzboardConfig:
    # Generator config
    attr_names: list[str]
    chart_type: list[str]
    trs_type: list[str | None]
    chart_map: dict[ChartKeyTokens, type]

    robustness: int

    # Explorer config
    n_epoch: int
    n_candidates: int
    n_search_space: int
    n_beam: int
    halving_ratio: float

    n_min_charts: int

    # Oracle Config
    weight: OracleWeight
    all_charts: list["BaseChart"]

    def __init__(
        self,
        df: pd.DataFrame,
        robustness: int = 1,
        n_epoch: int = 20,
        n_candidates: int = 50,
        halving_ratio: float = 0.2,
        n_search_space: int = 100,
        n_beam: int = 5,
        n_min_charts: int = 3,
        acceleration: float = 1,
    ) -> None:
        self.robustness = robustness
        self.n_epoch = n_epoch
        self.n_candidates = n_candidates
        self.chart_map = ChartMap
        self.halving_ratio = halving_ratio
        self.n_search_space = n_search_space
        self.n_beam = n_beam
        self.acceleration = acceleration
        self.n_min_charts = n_min_charts
        self.df = df
        self.weight = OracleWeight()
        self.all_charts = []
        self.init_constraints()
        self.raw_attr_names = [
            col
            for col in self.df.columns
            if (self.df[col].dtype == "object" and self.df[col].nunique() < 10)
            or self.df[col].dtype != "object"
            or "date" in col.lower()
            or "날짜" in col.lower()
        ]
        self.raw_attrs = [Attribute(None, None)] + [
            Attribute(
                col,
                "T"
                if "date" in col.lower() or "날짜" in col.lower()
                else "N"
                if self.df[col].dtype == "object"
                else "Q",
            )
            for col in self.raw_attr_names
        ]
        self.update_constraints(["arc", "sum", "min", "max", "tick", "day"])

    def init_constraints(self):
        self.attr_names = [
            col
            for col in self.df.columns
            if (self.df[col].dtype == "object" and self.df[col].nunique() < 10)
            or self.df[col].dtype != "object"
            or "date" in col.lower()
            or "날짜" in col.lower()
        ]
        self.df = self.df[self.attr_names]
        self.attrs = self.get_attrs()
        self.attr_types = [a.type for a in self.attrs]
        self.chart_type = list(set([m[0] for m in ChartMap]))
        self.txs = list(set([m[4] for m in ChartMap]))
        self.tys = list(set([m[5] for m in ChartMap]))
        self.tzs = list(set([m[6] for m in ChartMap]))
        self.trs_type = list(set(self.txs + self.tys + self.tzs))
        self.chart_map = ChartMap

    def get_attrs(self) -> list[Attribute]:
        return [Attribute(None, None)] + [
            Attribute(
                col,
                "T"
                if "date" in col.lower() or "날짜" in col.lower()
                else "N"
                if self.df[col].dtype == "object"
                else "Q",
            )
            for col in self.attr_names
        ]

    def get_chart_map(self) -> ChartMapType:
        def get_type(counter: Counter, key: str) -> int:
            return counter[key] if key in counter else 0

        filtered_chart_map = {
            key: value
            for key, value in ChartMap.items()
            if key[0] in self.chart_type
            and key[4] in self.trs_type
            and key[5] in self.trs_type
            and key[6] in self.trs_type
        }
        attr_types = [a.type for a in self.get_attrs() if a.type]
        attr_type_counter = Counter(attr_types)
        filtered_chart_map = {
            key: value
            for key, value in filtered_chart_map.items()
            if get_type(Counter(key), "N") <= attr_type_counter["N"]
            and get_type(Counter(key), "Q") <= attr_type_counter["Q"]
            and get_type(Counter(key), "T") <= attr_type_counter["T"]
        }
        return filtered_chart_map

    def update_constraints(self, constraints: list[str]):
        self.init_constraints()
        self.attr_names = [m for m in self.attr_names if m not in constraints]
        self.attrs = self.get_attrs()
        self.chart_type = [m for m in self.chart_type if m not in constraints]
        self.txs = [m for m in self.txs if m not in constraints]
        self.tys = [m for m in self.tys if m not in constraints]
        self.tzs = [m for m in self.tzs if m not in constraints]
        self.trs_type = list(set(self.txs + self.tys + self.tzs))
        self.chart_map = self.get_chart_map()
        self.all_charts = self.get_all_charts()

    def get_all_charts(self) -> list["BaseChart"]:
        all_charts = []
        typename = {
            "Q": [a.name for a in self.attrs if a.type == "Q"],
            "N": [a.name for a in self.attrs if a.type == "N"],
            "T": [a.name for a in self.attrs if a.type == "T"],
            None: [None],
        }
        chart_map = self.get_chart_map()
        for map in chart_map:
            for x_name in typename[map[1]]:
                for y_name in typename[map[2]]:
                    if y_name == x_name:
                        continue
                    for z_name in typename[map[3]]:
                        if z_name == x_name or (
                            z_name == y_name and z_name is not None
                        ):
                            continue

                        all_charts.append(
                            (
                                map[0],
                                x_name,
                                y_name,
                                z_name,
                                map[4],
                                map[5],
                                map[6],
                            )
                        )

        return [get_chart_from_tokens(k, self) for k in all_charts]

    def update_weight(
        self,
        specificity: float | None = None,
        interestingness: float | None = None,
        coverage: float | None = None,
        diversity: float | None = None,
        parsimony: float | None = None,
    ) -> bool:
        updated = False
        if specificity is not None and self.weight.specificity != specificity:
            self.weight.specificity = specificity
            updated = True
        if (
            interestingness is not None
            and self.weight.interestingness != interestingness
        ):
            self.weight.interestingness = interestingness
            updated = True
        if coverage is not None and self.weight.coverage != coverage:
            self.weight.coverage = coverage
            updated = True
        if diversity is not None and self.weight.diversity != diversity:
            self.weight.diversity = diversity
            updated = True
        if parsimony is not None and self.weight.parsimony != parsimony:
            self.weight.parsimony = parsimony
            updated = True
        return updated
