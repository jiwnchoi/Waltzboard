from typing import Optional
from dataclasses import dataclass
import pandas as pd

from gleaner.explorer import Explorer, TrainResult
from gleaner.generator import Generator
from gleaner.model import GleanerDashboard, BaseChart, ChartTokens
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

    def recommend(self, dashboard: GleanerDashboard, preferences: list[str], n_results: int = 5) -> list[BaseChart]:
        charts = self.generator.sample_n(200)
        filtered_charts = [c for c in charts if c.tokens not in [c.tokens for c in dashboard.charts]]
        candidate_dashboards = [GleanerDashboard(dashboard.charts + [c]) for c in filtered_charts]
        results = [self.oracle.get_result(d, set(preferences)) for d in candidate_dashboards]
        result_and_dashboards = [[r, d] for r, d in zip(results, candidate_dashboards)]
        result_and_dashboards.sort(key=lambda x: x[0].get_score(), reverse=True)
        return [d.charts for _, d in result_and_dashboards[:n_results]]
