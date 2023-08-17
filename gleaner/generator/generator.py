import numpy as np
import pandas as pd
from numpy.random import choice

from gleaner.config import GleanerConfig
from gleaner.generator import GeneratorConfig, PriorParameters
from gleaner.model import Attribute, GleanerChart, GleanerDashboard, get_gleaner_chart


def p(x: np.ndarray) -> np.ndarray:
    return x / x.sum()


def is_valid_map(current: list, map: list) -> bool:
    return all([map[i] == c.type if isinstance(c, Attribute) else map[i] == c for i, c in enumerate(current)])


class Generator:
    def __init__(self, config: "GleanerConfig") -> None:
        self.df = config.df
        self.attrs = [None] + config.attrs
        self.config = config
        self.prior = PriorParameters(self.config)

    def attr_mask(self, current: list["Attribute"]):
        valid_map = [e for e in self.config.chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array(
            [
                (e is None and e in valid_type)
                or (isinstance(e, Attribute) and e.type in valid_type and e not in current)
                for e in self.attrs
            ]
        )
        return weight_mask

    def ct_mask(self, current: list):
        valid_map = [e for e in self.config.chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in self.config.chart_type])
        return weight_mask

    def at_mask(self, current: list):
        valid_map = [e for e in self.config.chart_map if is_valid_map(current, e)]
        valid_type = set([e[len(current)] for e in valid_map])
        weight_mask = np.array([e in valid_type for e in self.config.agg_type])
        return weight_mask

    def sample_one(self) -> GleanerChart:
        current: list = []
        current.append(choice(self.config.chart_type, p=p(self.prior.ct.sample())))

        mask_x = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(self.prior.x.sample() * mask_x)))  # type: ignore

        mask_y = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(self.prior.y.sample() * mask_y)))  # type: ignore

        mask_z = self.attr_mask(current)
        current.append(choice(self.attrs, p=p(self.prior.z.sample() * mask_z)))  # type: ignore

        mask_at = self.at_mask(current)
        current.append(choice(self.config.agg_type, p=p(self.prior.at.sample() * mask_at)))

        return get_gleaner_chart(current, self.df)

    def sample_n(self, n: int) -> list[GleanerChart]:
        keys: set[str] = set()
        charts: list[GleanerChart] = []

        while len(charts) < n:
            chart = self.sample_one()
            if str(chart.sample) not in keys:
                keys.add(str(chart.sample))
                charts.append(chart)

        return charts

    def sample_dashboard(self, n: int) -> GleanerDashboard:
        return GleanerDashboard(self.sample_n(n))
