from typing import Optional
from dataclasses import dataclass
import pandas as pd

from gleaner.explorer import Explorer, TrainResult
from gleaner.generator import Generator
from gleaner.model import GleanerDashboard, BaseChart, ChartTokens
from gleaner.config import GleanerConfig
from gleaner.oracle import Oracle
from gleaner.utills import display_function
from gleaner.model import (
    is_valid_tokens,
    get_variants_from_charts,
    get_chart_from_tokens,
    get_all_charts,
)


class Gleaner:
    oracle: Oracle
    generator: Generator
    explorer: Explorer
    config: GleanerConfig
    preferences: list[str]

    def __init__(
        self, df: pd.DataFrame, config: GleanerConfig | None = None
    ) -> None:
        self.df = df
        if config and (df is not config.df):
            raise RuntimeError("df and config.df must be same")

        self.config = GleanerConfig(df)
        self.update_config()
        self.preferences = []

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

    def train(self, preferences: list[str]) -> list[TrainResult]:
        self.preferences = preferences
        return self.explorer.train(self.generator, self.oracle, preferences)

    def is_valid_tokens(self, key: ChartTokens):
        return is_valid_tokens(key, self.config)

    def get_variants_from_chart(self, chart: BaseChart):
        return get_variants_from_charts(chart, self.config)

    def get_chart_from_tokens(self, key: ChartTokens):
        if not self.is_valid_tokens(key):
            raise Exception("Chart tuple is not valid")
        return get_chart_from_tokens(key, self.config)

    def get_all_charts(self):
        return get_all_charts(self.config)
