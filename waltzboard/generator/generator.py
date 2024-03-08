from random import choices
from typing import TYPE_CHECKING

import numpy as np

from waltzboard.model import (
    Attribute,
    BaseChart,
    ChartKeyTokens,
    ChartSampled,
    ChartTokens,
    WaltzboardDashboard,
    get_chart_from_sample,
)

from .generator_parameters import PriorParameters

if TYPE_CHECKING:
    from waltzboard.config import WaltzboardConfig


def p(x: np.ndarray) -> np.ndarray:
    return x / x.sum()


def choice(a, p: np.ndarray) -> object:
    return choices(a, weights=p, k=1)[0]


def is_valid_map(current: list, map: ChartKeyTokens) -> bool:
    for i, c in enumerate(current):
        if isinstance(c, Attribute):
            if map[i] != c.type:
                return False
        elif map[i] != c:
            return False
    return True


def get_next_token_and_map(current: list, maps: list[ChartKeyTokens]):
    valid_maps = [e for e in maps if is_valid_map(current, e)]
    next_tokens = [e[len(current)] for e in valid_maps]
    return set(next_tokens), valid_maps


class Generator:
    def __init__(self, config: "WaltzboardConfig") -> None:
        self.df = config.df
        self.config = config
        self.prior = PriorParameters(self.config)
        self.chart_keys = self.config.get_chart_map().keys()

    def sample_one(self) -> BaseChart:
        current = []
        maps = self.config.chart_map
        it = {
            "ct": self.config.chart_type,
            "x": self.config.attrs,
            "y": self.config.attrs,
            "z": self.config.attrs,
            "tx": self.config.txs,
            "ty": self.config.tys,
            "tz": self.config.tzs,
        }

        for t, domain in it.items():
            next_tokens, maps = get_next_token_and_map(current, maps)
            mask = np.ones(len(domain))

            if t == "x":
                for i, token in enumerate(domain):
                    if token.type not in next_tokens:
                        mask[i] = 0

            elif t == "y":
                for i, token in enumerate(domain):
                    if token.type not in next_tokens:
                        mask[i] = 0
                    if token.name == current[1].name:
                        mask[i] = 0 if token.name is not None else 1

            elif t == "z":
                for i, token in enumerate(domain):
                    if token.type not in next_tokens:
                        mask[i] = 0
                    if token.name == current[1].name or token.name == current[2].name:
                        mask[i] = 0 if token.name is not None else 1

            else:
                for i, token in enumerate(domain):
                    if token not in next_tokens:
                        mask[i] = 0
            alpha = self.prior[t].sample()
            p_token = p(alpha * mask)
            current.append(choice(domain, p=p_token))

        sampled: ChartSampled = tuple(current)  # type: ignore
        return get_chart_from_sample(sampled, self.df)

    def sample_n(self, n: int) -> list[BaseChart]:
        keys: set[ChartTokens] = set()
        charts: list[BaseChart] = []

        limit = 0
        while len(charts) < n:
            limit += 1
            if limit > 10000:
                return charts

            chart = self.sample_one()

            if chart.tokens not in keys:
                keys.add(chart.tokens)
                charts.append(chart)

        return charts

    def sample_dashboard(self, n: int) -> WaltzboardDashboard:
        return WaltzboardDashboard(self.sample_n(n))
