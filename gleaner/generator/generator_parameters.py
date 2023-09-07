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
        c = np.random.dirichlet(self.count)
        if c.sum() == 0:
            print(c)
        return c


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
        sampled = np.random.normal(self.mean, np.sqrt(self.var))
        if sampled == np.nan:
            sampled = 0
        return np.max([sampled, 2])


class PriorParameters:
    ct: DirichletPrior
    x: DirichletPrior
    y: DirichletPrior
    z: DirichletPrior
    tx: DirichletPrior
    ty: DirichletPrior
    tz: DirichletPrior
    n_charts: NormalPrior

    def __init__(
        self,
        config: GleanerConfig,
    ) -> None:
        self.config = config
        self.ct = DirichletPrior(np.ones(len(self.config.chart_type)) * self.config.robustness)
        self.x = DirichletPrior(np.ones(len(self.config.attrs)) * self.config.robustness)
        self.y = DirichletPrior(np.ones(len(self.config.attrs)) * self.config.robustness)
        self.z = DirichletPrior(np.ones(len(self.config.attrs)) * self.config.robustness)
        self.tx = DirichletPrior(np.ones(len(self.config.txs)) * self.config.robustness)
        self.ty = DirichletPrior(np.ones(len(self.config.tys)) * self.config.robustness)
        self.tz = DirichletPrior(np.ones(len(self.config.tzs)) * self.config.robustness)
        self.n_charts = NormalPrior(len(self.config.attrs) - 1)

    def display(self):
        attribute_data = pd.DataFrame(
            {
                "x": self.x.count / np.sum(self.x.count),
                "y": self.y.count / np.sum(self.y.count),
                "z": self.z.count / np.sum(self.z.count),
            },
            index=[a.name for a in self.config.attrs],
        ).transpose()
        chart_type_data = pd.DataFrame(
            {"ct": self.ct.count / np.sum(self.ct.count)}, index=self.config.chart_type
        ).transpose()
        trs_type_data = pd.DataFrame(
            {
                "tx": self.tx.count / np.sum(self.tx.count),
                "ty": self.ty.count / np.sum(self.ty.count),
                "tz": self.tz.count / np.sum(self.tz.count),
            },
        ).transpose()
        display(self.n_charts.mean)
        display(attribute_data)
        display(chart_type_data)
        display(trs_type_data)

    def export(self):
        attrs = [
            {
                "name": str(attr.name),
                "x": self.x.count[i] / np.sum(self.x.count),
                "y": self.y.count[i] / np.sum(self.y.count),
                "z": self.z.count[i] / np.sum(self.z.count),
            }
            for i, attr in enumerate(self.config.attrs)
        ]
        cts = [
            {
                "name": ct,
                "prob": self.ct.count[i] / np.sum(self.ct.count),
            }
            for i, ct in enumerate(self.config.chart_type)
        ]
        ags = [
            {
                "name": str(at),
                "x": self.tx.count[self.config.txs.index(at)] / np.sum(self.tx.count) if at in self.config.txs else 0,
                "y": self.ty.count[self.config.tys.index(at)] / np.sum(self.ty.count) if at in self.config.tys else 0,
                "z": self.tz.count[self.config.tzs.index(at)] / np.sum(self.tz.count) if at in self.config.tzs else 0,
            }
            for at in self.config.trs_type
        ]
        return attrs, cts, ags
