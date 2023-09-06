import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import chi2_contingency

from .anova import f_oneway
from itertools import combinations

from gleaner.model import BaseChart, Attribute

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
    return "has_skewness" if abs(pd.to_numeric(df[attr].skew(skipna=True), errors="coerce")) > 2 else None


def has_kurtosis(df: pd.DataFrame, attr: str) -> str | None:
    return "has_kurtosis" if abs(pd.to_numeric(df[attr].kurtosis(skipna=True), errors="coerce")) > 7 else None


## NN
def has_correlation_nn(df: pd.DataFrame, attr1: str, attr2: str) -> str | None:
    contingency_table = pd.crosstab(df[attr1], df[attr2])
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return "has_correlation" if p_value < 0.05 else None


def has_outliers_nn(df: pd.DataFrame, attr1: str, attr2: str) -> str | None:
    contingency_table = pd.crosstab(df[attr1], df[attr2])
    chi2, p_value, _, expected = chi2_contingency(contingency_table)
    return (
        "has_outliers" if (p_value < 0.05 and np.count_nonzero(np.abs(contingency_table - expected) > 2) > 0) else None
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


hashmap: dict[str, list[str | None]] = {}
df_hash_map = {}


def mean(l):
    return sum(l) / len(l) if len(l) > 0 else 0


def get_statistic_features(node: "BaseChart") -> dict[str, list[str | None]]:
    attr_notnull = [attr for attr in node.attrs if attr.type != None and attr.type != "T"]
    attr_combinations: list[tuple[Attribute, ...]] = [
        *list(combinations(attr_notnull, 1)),
        *list(combinations(attr_notnull, 2)),
    ]
    features = {}
    if len(attr_notnull) == 0:
        return features
    for comb in attr_combinations:
        target_attrs: list[str] = [attr.name for attr in comb if attr.name]
        key = "/".join(target_attrs)

        try:
            if key not in hashmap:
                df_notnull = df_hash_map[key] if key in df_hash_map else node.df.dropna()
                if len(comb) == 1 and comb[0].type == "Q":
                    hashmap[key] = [
                        has_outliers_q(df_notnull, comb[0].name),
                        has_skewness_q(df_notnull, comb[0].name),
                        has_kurtosis(df_notnull, comb[0].name),
                    ]
                elif len(comb) == 1 and comb[0].type == "N":
                    hashmap[key] = [has_outliers_n(df_notnull, comb[0].name)]
                elif len(comb) == 2 and comb[0].type == "Q" and comb[1].type == "N":
                    hashmap[key] = [has_significance_qn(df_notnull, comb[0].name, comb[1].name)]
                elif len(comb) == 2 and comb[1].type == "Q" and comb[0].type == "N":
                    hashmap[key] = [has_significance_qn(df_notnull, comb[1].name, comb[0].name)]
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
            features[key] = hashmap[key]
        except Exception as e:
            print(f"Error in {key} with {comb}")
            raise e

    return features


def feature_to_interestingness(features: list[list[str | None]]) -> float:
    values = [bool(value) for feature in features for value in feature]
    return mean(values)


def get_interestingness(
    nodes: list["BaseChart"],
) -> float:
    node_features = [get_statistic_features(node) for node in nodes]

    return mean([feature_to_interestingness(list(feature.values())) for feature in node_features])
