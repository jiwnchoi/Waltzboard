import numpy as np
import pandas as pd
from numpy.random import choice

from gleaner.config import GleanerConfig
from gleaner.generator import PriorParameters
from gleaner.model import (
    Attribute,
    BaseChart,
    ChartKeyTokens,
    ChartSampled,
    GleanerDashboard,
    get_chart_from_sample,
)


def p(x: np.ndarray) -> np.ndarray:
    return x / x.sum()


def is_valid_map(current: list, map: ChartKeyTokens) -> bool:
    return all(
        [
            map[i] == c.type if isinstance(c, Attribute) else map[i] == c
            for i, c in enumerate(current)
        ]
    )


class Generator:
    def __init__(self, config: "GleanerConfig") -> None:
        self.df = config.df
        self.config = config
        self.prior = PriorParameters(self.config)
        self.chart_keys = self.config.get_chart_map().keys()

    def attr_mask(self, current: list):
        valid_map = [
            key for key in self.chart_keys if is_valid_map(current, key)
        ]
        valid_type = set([map[len(current)] for map in valid_map])
        weight_mask = np.array(
            [
                attr.type in valid_type
                and attr.name
                not in [
                    c.name
                    for c in current
                    if isinstance(c, Attribute) and c.name
                ]
                for attr in self.config.attrs
            ]
        )
        return weight_mask

    def ct_mask(self, current: list):
        valid_map = [e for e in self.chart_keys if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array(
            [e in valid_type for e in self.config.chart_type]
        )
        return weight_mask

    def at_mask(self, current: list):
        trss = (
            self.config.txs
            if len(current) == 4
            else self.config.tys
            if len(current) == 5
            else self.config.tzs
        )
        valid_map = [
            e for e in self.config.chart_map if is_valid_map(current, e)
        ]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in trss])
        return weight_mask

    def sample_one(self) -> BaseChart:
        current = []
        mask_ct = self.ct_mask(current)
        current.append(
            choice(
                self.config.chart_type, p=p(self.prior.ct.sample() * mask_ct)
            )
        )

        mask_x = self.attr_mask(current)
        current.append(
            choice(self.config.attrs, p=p(self.prior.x.sample() * mask_x))
        )

        mask_y = self.attr_mask(current)
        current.append(
            choice(self.config.attrs, p=p(self.prior.y.sample() * mask_y))
        )

        mask_z = self.attr_mask(current)
        current.append(
            choice(self.config.attrs, p=p(self.prior.z.sample() * mask_z))
        )

        mask_trs_x = self.at_mask(current)
        current.append(
            choice(self.config.txs, p=p(self.prior.tx.sample() * mask_trs_x))
        )

        mask_trs_y = self.at_mask(current)
        current.append(
            choice(self.config.tys, p=p(self.prior.ty.sample() * mask_trs_y))
        )

        mask_trs_z = self.at_mask(current)
        current.append(
            choice(self.config.tzs, p=p(self.prior.tz.sample() * mask_trs_z))
        )
        sampled: ChartSampled = tuple(current)
        return get_chart_from_sample(sampled, self.df)

    def sample_n(self, n: int) -> list[BaseChart]:
        keys: set[str] = set()
        charts: list[BaseChart] = []

        limit = 0
        while len(charts) < n:
            limit += 1
            if limit > 10000:
                print("Cannot sample enough charts", len(charts), n)
                break
            chart = self.sample_one()
            if str(chart.tokens) not in keys:
                keys.add(str(chart.tokens))
                charts.append(chart)

        return charts

    def sample_dashboard(self, n: int) -> GleanerDashboard:
        return GleanerDashboard(self.sample_n(n))
