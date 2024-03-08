from __future__ import annotations

import multiprocessing as mp
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import combinations
from os import cpu_count
from time import time
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.neighbors import LocalOutlierFactor

from .anova import f_oneway

if TYPE_CHECKING:
    from waltzboard.config import WaltzboardConfig
    from waltzboard.model import Attribute, BaseChart


@contextmanager
def poolcontext(*args, **kwargs):
    pool = mp.Pool(*args, **kwargs)
    yield pool
    pool.terminate()


lof = LocalOutlierFactor()


# N
def has_outliers_n(df: pd.DataFrame, attr: str) -> str | None:
    contingency_table = pd.crosstab(df[attr], columns="count")  # type: ignore
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return "has_outliers" if p_value < 0.05 else None


# Q
def has_outliers_q(df: pd.DataFrame, attr: str) -> str | None:
    pred = lof.fit_predict(df[attr].to_numpy().reshape(-1, 1))
    return "has_outliers" if np.count_nonzero(pred == -1) > 0 else None


def has_skewness_q(df: pd.DataFrame, attr: str) -> str | None:
    return (
        "has_skewness"
        if abs(pd.to_numeric(df[attr].skew(skipna=True), errors="coerce")) > 2
        else None
    )


def has_kurtosis(df: pd.DataFrame, attr: str) -> str | None:
    return (
        "has_kurtosis"
        if abs(pd.to_numeric(df[attr].kurtosis(skipna=True), errors="coerce")) > 7
        else None
    )


## NN
def has_correlation_nn(df: pd.DataFrame, attr1: str, attr2: str) -> str | None:
    contingency_table = pd.crosstab(df[attr1], df[attr2])
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return "has_correlation" if p_value < 0.05 else None


def has_outliers_nn(df: pd.DataFrame, attr1: str, attr2: str) -> str | None:
    contingency_table = pd.crosstab(df[attr1], df[attr2])
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return (
        "has_outliers"
        if (
            p_value < 0.05
            and np.count_nonzero(np.abs(contingency_table - expected) > 2) > 0
        )
        else None
    )


# QQ
def has_correlation_qq(df: pd.DataFrame, attr1: str, attr2: str) -> str | None:
    return "has_correlation" if df[attr1].corr(df[attr2]) ** 2 > 0.7 else None


def has_outliers_qq(df: pd.DataFrame, attr1: str, attr2: str) -> str | None:
    # use lof
    scores = lof.fit_predict(df[[attr1, attr2]])
    return "has_outliers" if np.count_nonzero(scores == -1) > 0 else None


## QN
def has_significance_qn(df: pd.DataFrame, attr_q: str, attr_n: str) -> str | None:
    n = df[attr_n].to_numpy()
    q = df[attr_q].to_numpy()
    f, p = f_oneway(n, q)
    return "has_significance" if p < 0.05 else None


stat_key = tuple[str] | tuple[str, str]
stats = list[str | None]

hashmap: dict[stat_key, stats] = {}
df_hash_map = {}


def mean(targets: list[float]):
    return sum(targets) / len(targets) if len(targets) > 0 else 0


@dataclass
class Statistics:
    key: stat_key
    features: stats

    def to_dict(self) -> dict[str, stat_key | stats]:
        return {
            "key": self.key,
            "features": self.features,
        }


def get_statistic_features(node: "BaseChart") -> dict[stat_key, stats]:
    attr_notnull = [
        attr for attr in node.attrs if attr.type is not None and attr.type != "T"
    ]
    attr_combinations: list[list["Attribute"]] = [
        [attr] for attr in attr_notnull if attr.name
    ] + [
        [attr1, attr2]
        for attr1, attr2 in combinations(attr_notnull, 2)
        if attr1.name and attr2.name and attr1.name != attr2.name
    ]
    keys = [tuple(attr.name for attr in comb) for comb in attr_combinations]
    featuers = {}
    for i, attrs in enumerate(attr_combinations):
        cached_features = hashmap.get(keys[i])
        # if not cached_features:
        #     print("not cached", keys[i])
        featuers[keys[i]] = (
            cached_features if cached_features else get_stats(node.df, attrs)
        )
    return featuers


def get_stats(df: pd.DataFrame, attrs: list["Attribute"]) -> stats:
    if len(attrs) == 1:
        key = ((attrs[0].name,) if attrs[0].name else "",)
        stats = get_stats_single(df, attrs)
        hashmap[key] = stats
        return stats
    elif len(attrs) == 2:
        keys = (
            (attrs[0].name if attrs[0].name else ""),
            (attrs[1].name if attrs[1].name else ""),
        )
        stats = get_stats_comb2(df, attrs)
        hashmap[keys[0]] = stats
        hashmap[keys[1]] = stats
        return stats


def get_stats_single(df: pd.DataFrame, attr: "Attribute") -> stats:
    attr = attr[0]
    name = attr.name if attr.name else ""
    key = (name,)
    df_notnull = df_hash_map[key] if key in df_hash_map else df[list(key)].dropna()
    df_hash_map[(name)] = df_notnull
    res: stats = []
    if attr.type == "N":
        res = [has_outliers_n(df_notnull, name)]
    elif attr.type == "Q":
        res = [
            has_outliers_q(df_notnull, name),
            has_skewness_q(df_notnull, name),
            has_kurtosis(df_notnull, name),
        ]
    return res


def get_stats_comb2(df: pd.DataFrame, comb: list["Attribute"]) -> stats:
    key = (
        comb[0].name if comb[0].name else "",
        comb[1].name if comb[1].name else "",
    )
    df_notnull = df_hash_map[key] if key in df_hash_map else df[list(key)].dropna()
    df_hash_map[key] = df_notnull
    df = df_notnull
    res: stats = []
    if comb[0].type == "Q" and comb[1].type == "N":
        res = [has_significance_qn(df, key[0], key[1])]
    elif comb[0].type == "N" and comb[1].type == "Q":
        res = [has_significance_qn(df, key[1], key[0])]
    elif comb[0].type == "Q" and comb[1].type == "Q":
        res = [
            has_correlation_qq(df, key[0], key[1]),
            has_outliers_qq(df, key[0], key[1]),
        ]
    elif comb[0].type == "N" and comb[1].type == "N":
        res = [
            has_correlation_nn(df, key[0], key[1]),
            has_outliers_nn(df, key[0], key[1]),
        ]
    return res


def get_statistics(node: "BaseChart") -> list[Statistics]:
    features = get_statistic_features(node)
    stats = [Statistics(key, value) for key, value in features.items()]
    return stats


def feature_to_interestingness(features: list[stats]) -> float:
    values = [bool(value) for feature in features for value in feature]
    return mean(values)


def get_interestingness(
    nodes: list["BaseChart"],
) -> float:
    node_features = [get_statistic_features(node) for node in nodes]

    intr = mean(
        [
            feature_to_interestingness(list(feature.values()))
            for feature in node_features
        ]
    )
    return intr


def hashing_stats(config: "WaltzboardConfig", parallelize=False):
    start = time()
    all_attrs = config.get_attrs()[1:]
    attrs = [[a] for a in all_attrs]
    attr_pairs = [list(comb) for comb in combinations(all_attrs, 2)]
    targets = attrs + attr_pairs
    iter = [(config.df, a) for a in targets]

    keys = [tuple(attr.name for attr in comb) for comb in targets]

    if all([key in hashmap for key in keys]):
        return hashmap

    if parallelize:
        with poolcontext(processes=cpu_count()) as pool:
            res = pool.starmap(get_stats, iter)
    else:
        res = [get_stats(i[0], i[1]) for i in iter]

    for i, target in enumerate(targets):
        if len(target) == 1:
            hashmap[(target[0].name,)] = res[i]
        else:
            hashmap[(target[0].name, target[1].name)] = res[i]
            hashmap[(target[1].name, target[0].name)] = res[i]
    print("hashing stats time", time() - start)
    return hashmap
