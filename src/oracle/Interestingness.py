from typing import TYPE_CHECKING
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


if TYPE_CHECKING:
    from ..space.Node import VISNode


# N
def get_outlierness_n(series: pd.Series, thresold: float = 1.5) -> float:
    counts = series.value_counts(normalize=True).to_numpy()
    entropy_vals = -np.sum(counts * np.log(counts), axis=1)
    return np.sum(entropy_vals < thresold) / len(entropy_vals)


# Q
def get_outlierness_q(series: pd.Series) -> float:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - iqr * iqr
    upper_bound = q3 + iqr * iqr
    outliers = (series < lower_bound) | (series > upper_bound)
    return len(outliers) / len(series)


def get_skewness_q(series: pd.Series) -> float:
    return min(abs(pd.to_numeric(series.skew(skipna=True), errors="coerce")), 2) / 2


def get_kurosis_q(series: pd.Series) -> float:
    return min(abs(pd.to_numeric(series.kurtosis(skipna=True), errors="coerce")), 7) / 7


def get_dispursion_q(series: pd.Series) -> float:
    return series.std() / series.mean()


# QQ
def get_correlation_qq(series1: pd.Series, series2: pd.Series) -> float:
    # return perason correlation
    return series1.corr(series2)


def get_outlierness_qq(series1: pd.Series, series2: pd.Series, k: int = 3) -> float:
    data = pd.concat([series1, series2], axis=1)
    X_std = StandardScaler().fit_transform(data)
    k_means = KMeans(n_clusters=k)
    k_means.fit(X_std)
    distances = k_means.transform(X_std)
    min_distances = np.min(distances, axis=1)
    thresold = 3 * np.std(min_distances)
    return np.sum(min_distances > thresold) / len(min_distances)


## QN


def get_interestingness_from_nodes(nodes: list["VISNode"], df: pd.DataFrame) -> float:
    return 1.0
