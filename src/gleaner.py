from dataclasses import dataclass
import pandas as pd

from src.explorer import Explorer, TrainResult
from src.generator import Generator
from src.model import GleanerDashboard
from src.config import GleanerConfig
from src.oracle import Oracle
from src.utill import display_function


class Gleaner:
    oracle: Oracle
    generator: Generator
    explorer: Explorer
    config: GleanerConfig
    preferences: list[str]

    def __init__(self, df: pd.DataFrame) -> None:
        self.config = GleanerConfig(df)
        self.oracle = Oracle(df)
        self.generator = Generator(df, self.config)
        self.explorer = Explorer(df, self.config)

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

    def infer(self) -> GleanerDashboard:
        return self.explorer.infer(self.generator, self.oracle, self.preferences)
