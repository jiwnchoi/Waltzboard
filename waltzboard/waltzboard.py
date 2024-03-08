from __future__ import annotations

import pandas as pd

from waltzboard.config import WaltzboardConfig
from waltzboard.explorer import Explorer, TrainResult
from waltzboard.generator import Generator
from waltzboard.model import (
    BaseChart,
    ChartTokens,
    get_chart_from_tokens,
    get_variants_from_charts,
    is_valid_tokens,
)
from waltzboard.oracle import Oracle
from waltzboard.oracle.scores.interestingness import hashing_stats
from waltzboard.utills import display_function


class Waltzboard:
    oracle: Oracle
    generator: Generator
    explorer: Explorer
    config: WaltzboardConfig
    preferences: list[str]
    constraints: list[str]
    need_train: bool
    train_results: list[TrainResult]

    def __init__(
        self,
        df: pd.DataFrame,
        config: WaltzboardConfig | None = None,
        parallelize=False,
    ) -> None:
        self.df = df
        self.config = WaltzboardConfig(df) if config is None else config
        self.update_config()
        self.preferences = []
        self.constraints = []
        self.need_train = True
        hashing_stats(self.config, parallelize)

    def update_constraints(self, constraints: list[str]) -> None:
        if len(set(constraints).intersection(set(self.constraints))) != len(
            constraints
        ):
            self.constraints = constraints
            self.config.update_constraints(constraints)
            self.update_config()
            self.need_train = True

    def update_preferences(self, preferences: list[str]) -> None:
        if set(preferences) != set(self.preferences):
            self.preferences = preferences
            self.need_train = True

    def update_weight(self, **kwargs) -> None:
        updated = self.config.update_weight(**kwargs)
        if updated:
            self.need_train = True
            self.update_config()

    def update_config(self):
        self.oracle = Oracle(self.config)
        self.generator = Generator(self.config)
        self.explorer = Explorer(self.config)

    def train_display(self, preferences: list[str]) -> None:
        self.preferences = preferences
        train_results: list[TrainResult] = []
        for epoch in range(self.config.n_epoch):
            train_result = self.explorer._train(
                self.generator, self.oracle, preferences
            )
            train_results.append(train_result)
            display_function(epoch, train_results)

    def train(self) -> list[TrainResult]:
        if len(self.config.all_charts) < self.config.n_search_space:
            self.train_results = []
            self.need_train = False
        if self.need_train:
            self.update_config()
            self.train_results = self.explorer.train(
                self.generator, self.oracle, self.preferences
            )
            self.need_train = False

        return self.train_results

    def is_valid_tokens(self, key: ChartTokens):
        return is_valid_tokens(key, self.config)

    def get_variants_from_chart(self, chart: BaseChart):
        return get_variants_from_charts(chart, self.config)

    def get_chart_from_tokens(self, key: ChartTokens):
        if not self.is_valid_tokens(key):
            print(key)
            raise Exception("Chart tuple is not valid")
        return get_chart_from_tokens(key, self.config)

    def get_all_charts(self):
        return self.config.all_charts
