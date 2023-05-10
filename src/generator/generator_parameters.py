import pandas as pd
from src.config import GleanerConfig
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

    def __init__(
        self,
        config: GleanerConfig,
    ) -> None:
        self.config = config

        attrs = [None] + self.config.attr_names
        self.x = DirichletPrior(np.ones(len(attrs)) * self.config.robustness)
        self.y = DirichletPrior(np.ones(len(attrs)) * self.config.robustness)
        self.z = DirichletPrior(np.ones(len(attrs)) * self.config.robustness)
        self.ct = DirichletPrior(
            np.ones(len(self.config.chart_type)) * self.config.robustness
        )
        self.at = DirichletPrior(
            np.ones(len(self.config.agg_type)) * self.config.robustness
        )
        self.n_charts = NormalPrior(len(attrs) - 1)

    def display(self):
        attribute_data = pd.DataFrame(
            {
                "x": self.x.count / np.sum(self.x.count),
                "y": self.y.count / np.sum(self.y.count),
                "z": self.z.count / np.sum(self.z.count),
            },
            index=self.attrs,
        ).transpose()
        chart_type_data = pd.DataFrame(
            {"ct": self.ct.count / np.sum(self.ct.count)}, index=self.config.chart_type
        ).transpose()
        agg_type_data = pd.DataFrame(
            {"at": self.at.count / np.sum(self.at.count)}, index=self.config.agg_type
        ).transpose()
        display(self.n_charts.mean)
        display(attribute_data)
        display(chart_type_data)
        display(agg_type_data)
