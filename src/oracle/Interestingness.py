from typing import TYPE_CHECKING
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import chi2_contingency, f_oneway, entropy
from itertools import combinations
from src.space.DataModel import Attribute, VisualizableDataFrame

if TYPE_CHECKING:
    from ..space.Node import VisualizationNode


# N
def has_outliers_n(df: pd.DataFrame, attr: str) -> bool:
    contingency_table = pd.crosstab(df[attr], columns="count")  # type: ignore
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return p_value < 0.05


# Q
def has_outliers_q(df: pd.DataFrame, attr: str) -> bool:
    lof = LocalOutlierFactor()
    pred = lof.fit_predict(df[attr].to_numpy().reshape(-1, 1))
    return np.count_nonzero(pred == -1) > 0


def has_skewness_q(df: pd.DataFrame, attr: str) -> bool:
    return abs(pd.to_numeric(df[attr].skew(skipna=True), errors="coerce")) > 2


def has_kurosis(df: pd.DataFrame, attr: str) -> bool:
    return abs(pd.to_numeric(df[attr].kurtosis(skipna=True), errors="coerce")) > 7


## NN
def has_correlation_nn(df: pd.DataFrame, attr1: str, attr2: str) -> bool:
    contingency_table = pd.crosstab(df[attr1], df[attr2])
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return p_value < 0.05


def has_outliers_nn(df: pd.DataFrame, attr1: str, attr2: str) -> bool:
    contingency_table = pd.crosstab(df[attr1], df[attr2])
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return (
        p_value < 0.05
        and np.count_nonzero(np.abs(contingency_table - expected) > 2) > 0
    )


# QQ
def has_correlation_qq(df: pd.DataFrame, attr1: str, attr2: str) -> bool:
    return df[attr1].corr(df[attr2]) ** 2 > 0.7


def has_outliers_qq(df: pd.DataFrame, attr1: str, attr2: str) -> bool:
    # use lof
    lof = LocalOutlierFactor()
    scores = lof.fit_predict(df[[attr1, attr2]])
    return np.count_nonzero(scores == -1) > 0


## QN
def has_significance_qn(df: pd.DataFrame, attr_q: str, attr_n: str) -> bool:
    grouped_data = [df[df[attr_n] == group][attr_q] for group in df[attr_n]]
    f_statistic, p_value = f_oneway(*grouped_data)
    return p_value < 0.05


HashMap = dict[str, list[bool]]


def get_statistic_feature_hashmap(
    vis_dfs: list[VisualizableDataFrame],
) -> HashMap:
    hashmap: HashMap = {}

    for vis_df in vis_dfs:
        attr_combinations: list[tuple[Attribute, ...]] = [
            *list(combinations(vis_df.attrs, 1)),
            *list(combinations(vis_df.attrs, 2)),
        ]
        for comb in attr_combinations:
            key = f"{((f[0], f[1] ) for f in vis_df.filter) if vis_df.filter is not None else ()}/"
            target_attrs = [attr.name for attr in comb]
            key += f"{target_attrs}"
            df_notnull = vis_df.df[target_attrs].dropna()
            if key not in hashmap:
                if len(comb) == 1 and comb[0].type == "Q":
                    hashmap[key] = [
                        has_outliers_q(df_notnull, comb[0].name),
                        has_skewness_q(df_notnull, comb[0].name),
                        has_kurosis(df_notnull, comb[0].name),
                    ]
                elif len(comb) == 1 and comb[0].type == "N":
                    hashmap[key] = [has_outliers_n(df_notnull, comb[0].name)]
                elif len(comb) == 2 and comb[0].type == "Q" and comb[1].type == "N":
                    hashmap[key] = [
                        has_significance_qn(df_notnull, comb[0].name, comb[1].name)
                    ]
                elif len(comb) == 2 and comb[1].type == "Q" and comb[0].type == "N":
                    hashmap[key] = [
                        has_significance_qn(df_notnull, comb[1].name, comb[0].name)
                    ]
                elif len(comb) == 2 and comb[0].type == "Q" and comb[1].type == "Q":
                    hashmap[key] = [
                        has_correlation_qq(df_notnull, comb[0].name, comb[1].name),
                        has_outliers_qq(df_notnull, comb[0].name, comb[1].name),
                    ]
                elif len(comb) == 2 and comb[0].type == "N" and comb[1].type == "N":
                    hashmap[key] = [
                        has_correlation_nn(df_notnull, comb[0].name, comb[1].name),
                        has_outliers_nn(df_notnull, comb[0].name, comb[1].name),
                    ]

    return hashmap


def get_statistic_features_from_node(
    node: "VisualizationNode", hashmap: HashMap
) -> list[list[bool]]:
    attr_combinations: list[tuple[Attribute, ...]] = [
        *list(combinations(node.attrs, 1)),
        *list(combinations(node.attrs, 2)),
    ]
    features = [
        hashmap[
            f"{((f[0], f[1] ) for f in node.filters) if node.filters is not None else ()}/{[attr.name for attr in comb]}"
        ]
        for comb in attr_combinations
    ]

    return features


mean = lambda x: sum(x) / len(x)


def get_interestingness(features: list[list[bool]]) -> float:
    values = [value for feature in features for value in feature]
    return mean(values)


def get_interestingness_from_nodes(
    nodes: list["VisualizationNode"], hashmap: HashMap
) -> float:
    node_features = [get_statistic_features_from_node(node, hashmap) for node in nodes]
    return mean([get_interestingness(feature) for feature in node_features])
