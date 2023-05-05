from dataclasses import dataclass
from collections import Counter
import pandas as pd
import numpy as np
from . import ExplorerConfig
from src.generator import Generator
from src.oracle import Oracle, OracleResult
from src.model import VisualizationNode
from src.ChartMap import chart_type, agg_type


def mean(l):
    return sum(l) / len(l)


class PosteriorCounter(Counter):
    def __init__(self, names):
        super().__init__({n: 0 for n in names})

    def get_posteriors(self, names):
        return np.array([self[n] for n in names])


class Counters:
    def __init__(self, attr_names):
        self.attr_names = attr_names
        self.x = PosteriorCounter(attr_names)
        self.y = PosteriorCounter(attr_names)
        self.z = PosteriorCounter(attr_names)
        self.ct = PosteriorCounter(attr_names)
        self.at = PosteriorCounter(attr_names)

    def update(self, node: VisualizationNode):
        ct, x, y, z, at = node.sample
        self.ct[ct] += 1
        self.x[x] += 1
        self.y[y] += 1
        self.z[z] += 1
        self.at[at] += 1


@dataclass
class TrainResult:
    scores: np.ndarray
    specificity: np.ndarray
    interestingness: np.ndarray
    coverage: np.ndarray
    diversity: np.ndarray
    conciseness: np.ndarray
    n_charts: np.ndarray


class Explorer:
    config: ExplorerConfig
    df: pd.DataFrame
    result: OracleResult | None = None

    def __init__(self, df: pd.DataFrame, config: ExplorerConfig) -> None:
        self.df = df
        self.config = config

    def train(self, gen: Generator, oracle: Oracle, wildcard: list[str]) -> TrainResult:
        n_charts: list[float] = [
            gen.prior.n_charts.sample() for _ in range(self.config.n_candidates)
        ]
        candidates: list[list[VisualizationNode]] = [
            gen.sample_n(round(n_chart)) for n_chart in n_charts
        ]
        results: list[OracleResult] = [
            oracle.get_result(dashboard, set(wildcard)) for dashboard in candidates
        ]

        specificity = np.array([])
        interestingness = np.array([])
        coverage = np.array([])
        diversity = np.array([])
        conciseness = np.array([])

        for r in results:
            specificity = np.append(specificity, r.specificity)
            interestingness = np.append(interestingness, r.interestingness)
            coverage = np.append(coverage, r.coverage)
            diversity = np.append(diversity, r.diversity)
            conciseness = np.append(conciseness, r.conciseness)

        raw_scores = specificity + interestingness + coverage + diversity + conciseness

        self.result = (
            results[np.argmax(raw_scores)]
            if self.result is None or max(raw_scores) > self.result.get_score()
            else self.result
        )

        normalized_scores = (
            (specificity - specificity.mean()) / specificity.std()
            + (interestingness - interestingness.mean()) / interestingness.std()
            + (coverage - coverage.mean()) / coverage.std()
            + (diversity - diversity.mean()) / diversity.std()
            + (conciseness - conciseness.mean()) / conciseness.std()
        )

        result_n_scores: list[tuple[OracleResult, float, float]] = [
            (r, raw_scores[i], normalized_scores[i]) for i, r in enumerate(results)
        ]
        sorted_result_n_scores = sorted(
            result_n_scores, key=lambda x: x[-1], reverse=True
        )

        halved_results = sorted_result_n_scores[
            : self.config.n_candidates // self.config.halving_ratio
        ]
        halved_n_charts = np.array([len(r[0].dashboard) for r in halved_results])

        counters = Counters(gen.attr_names)
        for candidate in halved_results:
            for chart in candidate[0].dashboard:
                counters.update(chart)

        gen.prior.x.update(counters.x.get_posteriors(gen.attr_names))
        gen.prior.y.update(counters.y.get_posteriors(gen.attr_names))
        gen.prior.z.update(counters.z.get_posteriors(gen.attr_names))
        gen.prior.ct.update(counters.ct.get_posteriors(gen.attr_names))
        gen.prior.at.update(counters.at.get_posteriors(gen.attr_names))
        gen.prior.n_charts.update(
            len(halved_n_charts), halved_n_charts.mean(), halved_n_charts.std()
        )

        return TrainResult(
            raw_scores,
            specificity,
            interestingness,
            coverage,
            diversity,
            conciseness,
            np.array([len(d) for d in candidates]),
        )
