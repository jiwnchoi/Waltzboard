from typing import Optional
from dataclasses import dataclass
import pandas as pd

from gleaner.explorer import Explorer, TrainResult
from gleaner.generator import Generator
from gleaner.model import GleanerDashboard, GleanerChart
from gleaner.config import GleanerConfig
from gleaner.oracle import Oracle
from gleaner.utill import display_function


class Gleaner:
    oracle: Oracle
    generator: Generator
    explorer: Explorer
    config: GleanerConfig
    preferences: list[str]

    def __init__(self, df: pd.DataFrame, config: GleanerConfig | None = None) -> None:
        self.df = df
        if config and (df is not config.df):
            raise RuntimeError("df and config.df must be same")

        self.config = GleanerConfig(df) if not config else config
        self.update_config()

    def update_config(self):
        self.oracle = Oracle(self.config)
        self.generator = Generator(self.config)
        self.explorer = Explorer(self.config)

    def train_display(self, preferences: list[str]) -> None:
        self.preferences = preferences
        train_results: list[TrainResult] = []
        for epoch in range(self.config.n_epoch):
            train_result = self.explorer._train(self.generator, self.oracle, preferences)
            train_results.append(train_result)
            display_function(epoch, train_results)

    def train(self, preferences: list[str]) -> list[TrainResult]:
        self.preferences = preferences
        return self.explorer.train(self.generator, self.oracle, preferences)

    def infer(self, n_chart: int | None = None, fixed_charts: list[list[str | None]] = []) -> GleanerDashboard:
        return self.explorer.infer(self.generator, self.oracle, self.preferences, n_chart, fixed_charts)

    def recommend(self, dashboard: GleanerDashboard, n_results: int = 5) -> list[GleanerChart]:
        inferred_charts = self.explorer._infer(
            self.generator,
            self.oracle,
            self.preferences,
            n_chart=len(dashboard) + 1,
            fixed_charts=dashboard.charts,
        )[0][:n_results]

        return [d[1].charts[-1] for d in inferred_charts]
