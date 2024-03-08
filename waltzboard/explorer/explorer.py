from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from random import choice
from typing import Optional

import numpy as np
import pandas as pd

from waltzboard.config import WaltzboardConfig
from waltzboard.generator import Generator
from waltzboard.model import BaseChart, ChartTokens, WaltzboardDashboard
from waltzboard.oracle import Normalizer, Oracle, OracleResult

from .explorer_result import TrainResult


def mean(target: list[float] | np.ndarray) -> float:
    return sum(target) / len(target)


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


class Explorer:
    config: WaltzboardConfig
    df: pd.DataFrame
    dashboard: WaltzboardDashboard | None
    result: OracleResult | None
    normalizer: Normalizer

    def __init__(self, config: "WaltzboardConfig"):
        self.df = config.df
        self.config = config
        self.dashboard = None
        self.result = None

    def _infer(
        self,
        gen: Generator,
        oracle: Oracle,
        preferences: list[str],
        n_chart: int | None = None,
        fixed_charts: list[BaseChart] = [],
    ):
        if n_chart and n_chart < len(fixed_charts):
            raise ValueError("Number of fixed_charts should be smaller than n_chart")

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
            oracle.get_result(dashboard, set(preferences)) for dashboard in candidates
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

        # # check self has property normalizer
        if not hasattr(self, "normalizer"):
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
            self.normalizer.normalize(specificity, "specificity")
            * oracle.weight.specificity
            + self.normalizer.normalize(interestingness, "interestingness")
            * oracle.weight.interestingness
            + self.normalizer.normalize(coverage, "coverage") * oracle.weight.coverage
            + self.normalizer.normalize(diversity, "diversity")
            * oracle.weight.diversity
            + self.normalizer.normalize(parsimony, "parsimony")
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
        if self.result is None or raw_scores[idx] < self.result.get_normalized_score(
            normalizer=self.normalizer
        ):
            self.dashboard = result_n_scores[idx][1]
            self.result = result_n_scores[idx][0]

        result_n_scores = sorted(result_n_scores, key=lambda x: x[-1], reverse=True)

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
    ) -> list["TrainResult"]:
        results = []
        for _ in range(self.config.n_epoch):
            results.append(self._train(gen, oracle, preferences))
        return results

    def search(
        self,
        gen: Generator,
        oracle: Oracle,
        preferences: list[str],
        fixed_charts: list[BaseChart] = [],
    ):
        # To set normalizer
        if not hasattr(self, "normalizer") or self.normalizer is None:
            self._infer(gen, oracle, preferences, fixed_charts=[])

        def _beam_search(current: list[list[BaseChart]], space: list[BaseChart]):
            leaves = [c + [s] for c in current for s in space if s not in c]
            scores = [
                oracle.get_result(
                    WaltzboardDashboard(leaf), set(preferences)
                ).get_normalized_score(normalizer=self.normalizer)
                * gen.prior.n_charts.score(len(leaf), len(self.config.attr_names) - 1)
                for leaf in leaves
            ]

            # scores = [
            #     oracle.get_result(
            #         WaltzboardDashboard(leaf), set(preferences)
            #     ).get_score()
            #     for leaf in leaves
            # ]
            next_indices = np.argsort(scores)[-self.config.n_beam :]
            next_leaves, next_scores = (
                [leaves[i] for i in next_indices],
                [scores[i] for i in next_indices],
            )
            return next_leaves, next_scores

        search_space = gen.sample_n(self.config.n_search_space)
        if len(search_space) < self.config.n_beam:
            return WaltzboardDashboard(search_space), oracle.get_result(
                WaltzboardDashboard(search_space), set(preferences)
            )

        pairs = [
            [*fixed_charts, *comb]
            for comb in combinations(search_space, max(0, 2 - len(fixed_charts)))
        ]
        pairs_scores = [
            oracle.get_result(
                WaltzboardDashboard(pair), set(preferences)
            ).get_normalized_score(normalizer=self.normalizer)
            * gen.prior.n_charts.score(len(pair), len(self.config.attr_names) - 1)
            for pair in pairs
        ]
        # pairs_scores = [
        #     oracle.get_result(
        #         WaltzboardDashboard(pair), set(preferences)
        #     ).get_score()
        #     for pair in pairs
        # ]
        root_indices = np.argsort(pairs_scores)[-self.config.n_beam :]
        leaves, scores = (
            [pairs[i] for i in root_indices],
            [pairs_scores[i] for i in root_indices],
        )
        limit = 0
        while True and limit < 100:
            next_leaves, next_scores = _beam_search(leaves, search_space)
            if (
                len(next_leaves[0]) > self.config.n_min_charts
                and len(next_scores)
                and next_scores[-1] < scores[0]
            ):
                break
            leaves, scores = next_leaves, next_scores
            limit += 1
        return WaltzboardDashboard(leaves[-1]), oracle.get_result(
            WaltzboardDashboard(leaves[-1]), set(preferences)
        )


TREE_WIDTH = 100
TERMINAL_THRESHOLD = 2
WEIGHT = 10


class MCTSExplorer:
    # Explorer with Monte Carlo Tree Search

    config: WaltzboardConfig
    df: pd.DataFrame
    dashboard: WaltzboardDashboard | None
    result: OracleResult | None
    normalizer: Normalizer

    def __init__(self, config: "WaltzboardConfig"):
        self.df = config.df
        self.config = config
        self.dashboard = None
        self.result = None

        self.Q = defaultdict(float)
        self.N = defaultdict(int)
        self.children = dict()

    def _uct_select(self, node: "MCTSNode"):
        assert all(n in self.children for n in self.children[node])

        def uct(n):
            return self.Q[n] / self.N[n] + WEIGHT * np.sqrt(
                np.log(self.N[node]) / self.N[n]
            )

        return max(self.children[node], key=uct)

    def _backpropagate(self, path: list["MCTSNode"], reward: float):
        for node in path:
            self.N[node] += 1
            self.Q[node] += reward

    def _simulate(self, node: "MCTSNode"):
        while not node.is_terminal():
            node = node.get_child()
        return node.reward()

    def _expand(self, node: "MCTSNode"):
        if node.is_terminal():
            return set()

        return {node.get_child() for _ in range(TREE_WIDTH)}

    def _select(self, node: "MCTSNode"):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)

    def do_rollout(self, node: "MCTSNode"):
        path = self._select(node)
        leaf = path[-1]
        self.children[leaf] = self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def choose(self, node: "MCTSNode"):
        if node.is_terminal():
            raise RuntimeError("choose called on terminal node")
        if node not in self.children:
            return node.get_child()

        def score(node: "MCTSNode"):
            if self.N[node] == 0:
                return float("-inf")
            return node.reward()

        return max(self.children[node], key=score)


class MCTSNode:
    charts: list[BaseChart]
    vocab: list[ChartTokens]
    terminal_count: int
    score: float

    config: WaltzboardConfig
    oracle: Oracle
    preferences: list[str]

    def __init__(
        self,
        config: WaltzboardConfig,
        oracle: Oracle,
        preferences: list[str] = [],
        charts: list[BaseChart] = [],
        parent: Optional["MCTSNode"] = None,
    ):
        self.charts = charts
        self.vocab = [tuple([str(t) for t in c.tokens]) for c in charts]
        self.config = config
        self.oracle = oracle
        self.preferences = preferences
        self.terminal_count = 0
        self.score = self._reward()

        if parent and parent.score > self.score:
            self.terminal_count = parent.terminal_count + 1

    def __hash__(self):
        return hash(frozenset(sorted(self.vocab)))

    def __repr__(self) -> str:
        return f"<MCTSNode {self.vocab}>"

    def get_child(self):
        if self.is_terminal():
            return set()

        child = None
        while child is None or child.tokens in self.vocab:
            child = choice(self.config.all_charts)

        return MCTSNode(
            self.config,
            self.oracle,
            self.preferences,
            self.charts + [child],
            self,
        )

    def is_terminal(self):
        return (
            self.terminal_count >= TERMINAL_THRESHOLD
            and len(self.charts) >= self.config.n_min_charts
        )

    def _result(self) -> OracleResult:
        return self.oracle.get_result(
            WaltzboardDashboard(self.charts), set(self.preferences)
        )

    def _reward(self):
        if len(self.charts) <= self.config.n_min_charts:
            return 0

        return self._result().get_score()

    def reward(self):
        return self.score
