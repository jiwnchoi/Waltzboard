import pandas as pd
from dataclasses import dataclass
from src.ChartMap import chart_type, agg_type
import numpy as np
from IPython.display import display


class DirichletPrior:
    count: np.ndarray
    history: list[np.ndarray]

    def __init__(self, count: np.ndarray) -> None:
        self.count = count
        self.history = [count]

    def parameters(self):
        return self.count / np.sum(self.count)

    def update(self, x: np.ndarray):
        self.count += x
        self.history.append(np.copy(self.count))

    def sample(self):
        return np.random.dirichlet(self.count)


class NormalPrior:
    mean: float
    var: float = 1
    history: list[float]

    def __init__(self, mean: float) -> None:
        self.mean = mean
        self.history = [mean]

    def update(self, n, observed_mean, observed_var):
        self.mean = (self.mean / self.var + observed_mean * n / observed_var) / (
            1 / self.var + n / observed_var
        )
        # self.var = 1 / (1 / self.var + n / observed_var)
        self.history.append(self.mean)

    def sample(self):
        return max(np.random.normal(self.mean, np.sqrt(self.var)), 2)


class PriorParameters:
    x: DirichletPrior
    y: DirichletPrior
    z: DirichletPrior
    ct: DirichletPrior
    at: DirichletPrior
    n_charts: NormalPrior
    attrs: list[str | None]

    def __init__(self, attrs: list[str | None]) -> None:
        self.x = DirichletPrior(np.ones(len(attrs)))
        self.y = DirichletPrior(np.ones(len(attrs)))
        self.z = DirichletPrior(np.ones(len(attrs)))
        self.ct = DirichletPrior(np.ones(len(chart_type)))
        self.at = DirichletPrior(np.ones(len(agg_type)))
        self.n_charts = NormalPrior(len(attrs) - 1)
        self.attrs = attrs

    def display_parameter(self):
        print(f"N Charts: {self.n_charts.mean}")
        display(
            pd.DataFrame(
                {attr: self.x.parameters()[i] for i, attr in enumerate(self.attrs)}
            )
        )
        display(
            pd.DataFrame(
                {attr: self.y.parameters()[i] for i, attr in enumerate(self.attrs)}
            )
        )
        display(
            pd.DataFrame(
                {attr: self.z.parameters()[i] for i, attr in enumerate(self.attrs)}
            )
        )
        display(
            pd.DataFrame(
                {attr: self.ct.parameters()[i] for i, attr in enumerate(chart_type)}
            )
        )
        display(
            pd.DataFrame(
                {attr: self.at.parameters()[i] for i, attr in enumerate(agg_type)}
            )
        )
