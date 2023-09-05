import pandas as pd
from gleaner.config import GleanerConfig
from gleaner.model import Attribute
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
        r = np.sum(self.count)
        self.count += x
        self.count = self.count / np.sum(self.count) * r  # type: ignore
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
        self.mean = (self.mean / self.var + observed_mean * n / observed_var) / (1 / self.var + n / observed_var)
        # self.var = 1 / (1 / self.var + n / observed_var)
        self.history.append(self.mean)

    def sample(self):
        return max(np.random.normal(self.mean, np.sqrt(self.var)), 2)


class PriorParameters:
    ct: DirichletPrior
    x: DirichletPrior
    y: DirichletPrior
    z: DirichletPrior
    tx: DirichletPrior
    ty: DirichletPrior
    tz: DirichletPrior
    n_charts: NormalPrior
    attrs: list[Attribute]

    def __init__(
        self,
        config: GleanerConfig,
    ) -> None:
        self.config = config
        self.attrs = self.config.attrs
        self.ct = DirichletPrior(np.ones(len(self.config.chart_type)) * self.config.robustness)
        self.x = DirichletPrior(np.ones(len(self.attrs)) * self.config.robustness)
        self.y = DirichletPrior(np.ones(len(self.attrs)) * self.config.robustness)
        self.z = DirichletPrior(np.ones(len(self.attrs)) * self.config.robustness)
        self.tx = DirichletPrior(np.ones(len(self.config.txs)) * self.config.robustness)
        self.ty = DirichletPrior(np.ones(len(self.config.tys)) * self.config.robustness)
        self.tz = DirichletPrior(np.ones(len(self.config.tzs)) * self.config.robustness)
        self.n_charts = NormalPrior(len(self.attrs) - 1)

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
            {
                "tx": self.tx.count / np.sum(self.tx.count),
                "ty": self.ty.count / np.sum(self.ty.count),
                "tz": self.tz.count / np.sum(self.tz.count),
            },
        ).transpose()
        display(self.n_charts.mean)
        display(attribute_data)
        display(chart_type_data)
        display(agg_type_data)

    def export(self):
        attrs = [
            {
                "name": str(attr),
                "x": self.x.count[i] / np.sum(self.x.count),
                "y": self.y.count[i] / np.sum(self.y.count),
                "z": self.z.count[i] / np.sum(self.z.count),
            }
            for i, attr in enumerate(self.attrs)
        ]
        cts = [
            {
                "name": str(ct),
                "prob": self.ct.count[i] / np.sum(self.ct.count),
            }
            for i, ct in enumerate(self.config.chart_type)
        ]
        ags = [
            {
                "name": str(at),
                "x": self.tx.count[i] / np.sum(self.tx.count),
                "y": self.ty.count[i] / np.sum(self.ty.count),
                "z": self.tz.count[i] / np.sum(self.tz.count),
            }
            for i, at in enumerate(self.config.agg_type)
        ]
        return attrs, cts, ags
