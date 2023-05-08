from dataclasses import dataclass
from collections import Counter
import pandas as pd
import numpy as np
from src.explorer import ExplorerConfig, TrainResult
from src.generator import Generator
from src.oracle import Oracle, OracleResult
from src.model import GleanerChart, GleanerDashboard
from src.config import chart_type, agg_type


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

    def update(self, node: GleanerChart):
        ct, x, y, z, at = node.sample
        self.ct[ct] += 1
        self.x[x] += 1
        self.y[y] += 1
        self.z[z] += 1
        self.at[at] += 1


class Explorer:
    config: ExplorerConfig
    df: pd.DataFrame
    dashboard: GleanerDashboard | None = None
    result: OracleResult | None = None

    def __init__(self, df: pd.DataFrame, config: ExplorerConfig) -> None:
        self.df = df
        self.config = config

    def train(self, gen: Generator, oracle: Oracle, wildcard: list[str]) -> TrainResult:
        n_charts: list[float] = [
            gen.prior.n_charts.sample() for _ in range(self.config.n_candidates)
        ]
        candidates: list[GleanerDashboard] = [
            gen.sample_dashboard(round(n_chart)) for n_chart in n_charts
        ]
        results: list[OracleResult] = [
            oracle.get_result(dashboard, set(wildcard)) for dashboard in candidates
        ]

        specificity = np.array([r.specificity for r in results])
        interestingness = np.array([r.interestingness for r in results])
        coverage = np.array([r.coverage for r in results])
        diversity = np.array([r.diversity for r in results])
        conciseness = np.array([r.conciseness for r in results])

        raw_scores: np.ndarray = (
            specificity + interestingness + coverage + diversity + conciseness
        )

        normalized_scores = (
            (specificity - specificity.mean()) / specificity.std()
            + (interestingness - interestingness.mean()) / interestingness.std()
            + (coverage - coverage.mean()) / coverage.std()
            + (diversity - diversity.mean()) / diversity.std()
            + (conciseness - conciseness.mean()) / conciseness.std()
        )

        result_n_scores: list[tuple[OracleResult, GleanerDashboard, float, float]] = [
            (result, candidates[i], raw_scores[i], normalized_scores[i])
            for i, result in enumerate(results)
        ]
        result_n_scores = sorted(result_n_scores, key=lambda x: x[-1], reverse=True)

        halved_results = result_n_scores[
            0 : int(self.config.n_candidates * self.config.halving_ratio)
        ]
        halved_n_charts = np.array([len(r[1]) for r in halved_results])

        counters = Counters(gen.attr_names)
        for candidate in halved_results:
            charts = candidate[1].charts
            for chart in charts:
                counters.update(chart)

        gen.prior.x.update(counters.x.get_posteriors(gen.attr_names))
        gen.prior.y.update(counters.y.get_posteriors(gen.attr_names))
        gen.prior.z.update(counters.z.get_posteriors(gen.attr_names))
        gen.prior.ct.update(counters.ct.get_posteriors(chart_type))
        gen.prior.at.update(counters.at.get_posteriors(agg_type))
        gen.prior.n_charts.update(
            len(halved_n_charts), halved_n_charts.mean(), halved_n_charts.std()
        )

        expl_idx = np.argmax(normalized_scores)
        self.dashboard = candidates[expl_idx]
        self.result = (
            results[expl_idx]
            if self.result is None or raw_scores[expl_idx] > self.result.get_score()
            else self.result
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
