from dataclasses import dataclass
from src.ChartMap import chart_type, agg_type
import numpy as np


@dataclass
class DirichletPrior:
    count: np.ndarray

    def update(self, x):
        self.count += x

    def sample(self):
        return np.random.dirichlet(self.count)


@dataclass
class NormalPrior:
    mean: float
    var: float = 1

    def update(self, n, observed_mean, observed_var):
        self.mean = (self.mean / self.var + observed_mean * n / observed_var) / (
            1 / self.var + n / observed_var
        )
        self.var = 1 / (1 / self.var + n / observed_var)

    def sample(self):
        return np.random.normal(self.mean, np.sqrt(self.var))


class PriorParameters:
    x: DirichletPrior
    y: DirichletPrior
    z: DirichletPrior
    ct: DirichletPrior
    at: DirichletPrior
    n_chart: NormalPrior

    def __init__(self, attrs: list[str | None], n_chart: int) -> None:
        self.x = DirichletPrior(np.ones(len(attrs)))
        self.y = DirichletPrior(np.ones(len(attrs)))
        self.z = DirichletPrior(np.ones(len(attrs)))
        self.ct = DirichletPrior(np.ones(len(chart_type)))
        self.at = DirichletPrior(np.ones(len(agg_type)))
        self.n_chart = NormalPrior(float(n_chart))
