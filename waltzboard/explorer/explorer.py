from dataclasses import dataclass
from collections import Counter
from itertools import combinations

import numpy as np
import pandas as pd

from waltzboard.config import WaltzboardConfig
from waltzboard.explorer import TrainResult
from waltzboard.generator import Generator
from waltzboard.model import BaseChart, WaltzboardDashboard
from waltzboard.oracle import Oracle, OracleResult


def mean(l):
    return sum(l) / len(l)


class PosteriorCounter(Counter):
    def __init__(self, names):
        super().__init__({n: 0 for n in names})

    def get_posteriors(self):
        return np.array(list(self.values()))


class Counters:
    def __init__(self, config: WaltzboardConfig):
        self.ct = PosteriorCounter(config.chart_type)
        self.x = PosteriorCounter([None] + config.attr_names)
        self.y = PosteriorCounter([None] + config.attr_names)
        self.z = PosteriorCounter([None] + config.attr_names)
        self.tx = PosteriorCounter(config.txs)
        self.ty = PosteriorCounter(config.tys)
        self.tz = PosteriorCounter(config.tzs)

    def update(self, node: BaseChart):
        ct, x, y, z, tx, ty, tz = node.tokens
        self.ct[ct] += 1
        self.x[x] += 1
        self.y[y] += 1
        self.z[z] += 1
        self.tx[tx] += 1
        self.ty[ty] += 1
        self.tz[tz] += 1


@dataclass
class Normalizer:
    specificity_mean: float
    specificity_std: float
    interestingness_mean: float
    interestingness_std: float
    coverage_mean: float
    coverage_std: float
    diversity_mean: float
    diversity_std: float
    parsimony_mean: float
    parsimony_std: float

    def normalize(self, scores: np.ndarray, score_type: str):
        if score_type == 'specificity':
            s = (scores - self.specificity_mean) / self.specificity_std
        elif score_type == 'interestingness':
            s = (scores - self.interestingness_mean) / self.interestingness_std
        elif score_type == 'coverage':
            s = (scores - self.coverage_mean) / self.coverage_std
        elif score_type == 'diversity':
            s = (scores - self.diversity_mean) / self.diversity_std
        elif score_type == 'parsimony':
            s = (scores - self.parsimony_mean) / self.parsimony_std
        else:
            s = scores
        return s


class Explorer:
    config: WaltzboardConfig
    df: pd.DataFrame
    dashboard: WaltzboardDashboard | None
    result: OracleResult | None
    normalizer: Normalizer | None

    def __init__(self, config: "WaltzboardConfig"):
        self.df = config.df
        self.config = config
        self.dashboard = None
        self.result = None
        self.normalizer = None

    def _infer(
        self,
        gen: Generator,
        oracle: Oracle,
        preferences: list[str],
        n_chart: int | None = None,
        fixed_charts: list[BaseChart] = [],
    ):
        if n_chart and n_chart < len(fixed_charts):
            raise ValueError(
                "Number of fixed_charts should be smaller than n_chart"
            )

        n_charts: list[float] = [
            gen.prior.n_charts.sample() if n_chart is None else n_chart
            for _ in range(self.config.n_candidates)
        ]

        if len(fixed_charts):
            n_charts = [max(1, n - len(fixed_charts)) for n in n_charts]
        candidates: list[WaltzboardDashboard] = [
            gen.sample_dashboard(round(n_chart)) for n_chart in n_charts
        ]

        if len(fixed_charts):
            for candidate in candidates:
                candidate.extend(fixed_charts)

        results: list[OracleResult] = [
            oracle.get_result(dashboard, set(preferences))
            for dashboard in candidates
        ]

        specificity = np.array([r.specificity for r in results])
        interestingness = np.array([r.interestingness for r in results])
        coverage = np.array([r.coverage for r in results])
        diversity = np.array([r.diversity for r in results])
        parsimony = np.array([r.parsimony for r in results])

        raw_scores: np.ndarray = (
            specificity * oracle.weight.specificity
            + interestingness * oracle.weight.interestingness
            + coverage * oracle.weight.coverage
            + diversity * oracle.weight.diversity
            + parsimony * oracle.weight.parsimony
        )

        if self.normalizer is None:
            self.normalizer = Normalizer(
                specificity.mean(),
                specificity.std(),
                interestingness.mean(),
                interestingness.std(),
                coverage.mean(),
                coverage.std(),
                diversity.mean(),
                diversity.std(),
                parsimony.mean(),
                parsimony.std(),
            )

        normalized_scores: np.ndarray = (
            self.normalizer.normalize(specificity, 'specificity')
            * oracle.weight.specificity
            + self.normalizer.normalize(interestingness, 'interestingness')
            * oracle.weight.interestingness
            + self.normalizer.normalize(coverage, 'coverage')
            * oracle.weight.coverage
            + self.normalizer.normalize(diversity, 'diversity')
            * oracle.weight.diversity
            + self.normalizer.normalize(parsimony, 'parsimony')
            * oracle.weight.parsimony
        )

        result_n_scores: list[
            tuple[OracleResult, WaltzboardDashboard, float, float]
        ] = [
            (result, candidates[i], raw_scores[i], normalized_scores[i])
            for i, result in enumerate(results)
        ]

        result_n_scores.sort(key=lambda x: x[-1], reverse=True)

        return (
            result_n_scores,
            raw_scores,
            normalized_scores,
            specificity,
            interestingness,
            coverage,
            diversity,
            parsimony,
        )

    def _train(
        self, gen: Generator, oracle: Oracle, preferences: list[str]
    ) -> TrainResult:
        (
            result_n_scores,
            raw_scores,
            normalized_scores,
            specificity,
            interestingness,
            coverage,
            diversity,
            parsimony,
        ) = self._infer(gen, oracle, preferences)

        idx = np.argmax(raw_scores)
        if self.result is None or raw_scores[idx] < self.result.get_score():
            self.dashboard = result_n_scores[idx][1]
            self.result = result_n_scores[idx][0]

        result_n_scores = sorted(
            result_n_scores, key=lambda x: x[-1], reverse=True
        )

        halved_results = result_n_scores[
            0 : int(self.config.n_candidates * self.config.halving_ratio)
        ]
        halved_n_charts = np.array([len(r[1]) for r in halved_results])

        counters = Counters(self.config)
        for candidate in halved_results:
            charts = candidate[1].charts
            for chart in charts:
                counters.update(chart)

        gen.prior.x.update(counters.x.get_posteriors())
        gen.prior.y.update(counters.y.get_posteriors())
        gen.prior.z.update(counters.z.get_posteriors())
        gen.prior.ct.update(counters.ct.get_posteriors())
        gen.prior.tx.update(counters.tx.get_posteriors())
        gen.prior.ty.update(counters.ty.get_posteriors())
        gen.prior.tz.update(counters.tz.get_posteriors())
        gen.prior.n_charts.update(
            len(halved_n_charts), halved_n_charts.mean(), halved_n_charts.std()
        )

        return TrainResult(
            raw_scores,
            specificity,
            interestingness,
            coverage,
            diversity,
            parsimony,
            np.array([len(d[1]) for d in result_n_scores]),
        )

    def train(
        self, gen: Generator, oracle: Oracle, preferences: list[str]
    ) -> list[TrainResult]:
        results = []
        for _ in range(self.config.n_epoch):
            results.append(self._train(gen, oracle, preferences))
        return results

    def search(self, gen: Generator, oracle: Oracle, preferences: list[str], fixed_charts: list[BaseChart] = []):
        def _beam_search(
            current: list[list[BaseChart]], space: list[BaseChart]
        ):
            leaves = [c + [s] for c in current for s in space if s not in c]
            scores = [
                oracle.get_result(
                    WaltzboardDashboard(leaf), set(preferences)
                ).get_score()
                for leaf in leaves
            ]
            next_indices = np.argsort(scores)[-self.config.n_beam :]
            next_leaves, next_scores = [leaves[i] for i in next_indices], [
                scores[i] for i in next_indices
            ]
            return next_leaves, next_scores

        search_space = gen.sample_n(self.config.n_search_space)
        pairs = [
            [*fixed_charts ,search_space[i], search_space[j]]
            for i, j in combinations(range(len(search_space)), 2)
        ] 
        pairs_scores = [
            oracle.get_result(
                WaltzboardDashboard(pair), set(preferences)
            ).get_score()
            for pair in pairs
        ]
        root_indices = np.argsort(pairs_scores)[-self.config.n_beam :]
        leaves, scores = [pairs[i] for i in root_indices], [
            pairs_scores[i] for i in root_indices
        ]

        while True:
            next_leaves, next_scores = _beam_search(leaves, search_space)
            if next_scores[-1] < scores[0]:
                break
            leaves, scores = next_leaves, next_scores

        return WaltzboardDashboard(leaves[-1]), oracle.get_result(
            WaltzboardDashboard(leaves[-1]), set(preferences)
        )
