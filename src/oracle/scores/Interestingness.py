import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import chi2_contingency, f_oneway, entropy
from itertools import combinations

from src.model import GleanerChart, Attribute

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
    grouped_data = [df[df[attr_n] == group][attr_q] for group in df[attr_n]]
    f_statistic, p_value = f_oneway(*grouped_data)
    return "has_significance" if p_value < 0.05 else None


HashMap = dict[str, list[str | None]]

hashmap: HashMap = {}


def mean(l):
    return sum(l) / len(l)


def get_statistic_features(node: "GleanerChart") -> list[list[str | None]]:
    attr_combinations: list[tuple[Attribute, ...]] = [
        *list(combinations(node.attrs, 1)),
        *list(combinations(node.attrs, 2)),
    ]
    features = []
    for comb in attr_combinations:
        key = ""
        if node.filters is not None:
            for f in node.filters:
                key += f"{str((f[0], f[1]))}/"
        target_attrs = [attr.name for attr in comb]
        key += f"{target_attrs}"

        df_notnull = node.sub_df.dropna()
        try:
            if key not in hashmap:
                if len(comb) == 1 and comb[0].type == "Q":
                    hashmap[key] = [
                        has_outliers_q(df_notnull, comb[0].name),
                        has_skewness_q(df_notnull, comb[0].name),
                        has_kurtosis(df_notnull, comb[0].name),
                    ]
                elif len(comb) == 1 and comb[0].type == "C":
                    hashmap[key] = [has_outliers_n(df_notnull, comb[0].name)]
                elif len(comb) == 2 and comb[0].type == "Q" and comb[1].type == "C":
                    hashmap[key] = [
                        has_significance_qn(df_notnull, comb[0].name, comb[1].name)
                    ]
                elif len(comb) == 2 and comb[1].type == "Q" and comb[0].type == "C":
                    hashmap[key] = [
                        has_significance_qn(df_notnull, comb[1].name, comb[0].name)
                    ]
                elif len(comb) == 2 and comb[0].type == "Q" and comb[1].type == "Q":
                    hashmap[key] = [
                        has_correlation_qq(df_notnull, comb[0].name, comb[1].name),
                        has_outliers_qq(df_notnull, comb[0].name, comb[1].name),
                    ]
                elif len(comb) == 2 and comb[0].type == "C" and comb[1].type == "C":
                    hashmap[key] = [
                        has_correlation_nn(df_notnull, comb[0].name, comb[1].name),
                        has_outliers_nn(df_notnull, comb[0].name, comb[1].name),
                    ]
            features.append(hashmap[key])
        except Exception as e:
            print(f"Error in {key} with {comb} and {node.filters}")
            raise e

    return features


def feature_to_interestingness(features: list[list[str | None]]) -> float:
    values = [bool(value) for feature in features for value in feature]
    return mean(values)


def get_interestingness(
    nodes: list["GleanerChart"],
) -> float:
    node_features = [get_statistic_features(node) for node in nodes]

    return mean([feature_to_interestingness(feature) for feature in node_features])
