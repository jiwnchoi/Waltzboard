from typing import TYPE_CHECKING
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import chi2_contingency
from sklearn.linear_model import LogisticRegression

if TYPE_CHECKING:
    from ..space.Node import VisualizationNode


# N
def get_outlierness_n(series: pd.Series, thresold: float = 1.5) -> float:
    counts = series.value_counts(normalize=True).to_numpy()
    entropy_vals = -np.sum(counts * np.log(counts), axis=1)
    return np.count_nonzero(entropy_vals < thresold) / len(entropy_vals)


# Q
def get_outlierness_q(series: pd.Series) -> float:
    lof = LocalOutlierFactor()
    pred = lof.fit_predict(series.to_numpy().reshape(-1, 1))
    return np.count_nonzero(pred == -1) / len(pred)


def get_skewness_q(series: pd.Series) -> float:
    return min(abs(pd.to_numeric(series.skew(skipna=True), errors="coerce")), 2) / 2


def get_kurosis_q(series: pd.Series) -> float:
    return min(abs(pd.to_numeric(series.kurtosis(skipna=True), errors="coerce")), 7) / 7


def get_dispursion_q(series: pd.Series) -> float:
    return series.std() / series.mean()


## NN
def get_correlation_nn(series1: pd.Series, series2: pd.Series) -> float:
    # cramers_v
    confusion_matrix = pd.crosstab(series1, series2)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))


def get_outlierness_nn(series1: pd.Series, series2: pd.Series) -> float:
    # Point-wise Mutual Information
    crosstab = pd.crosstab(series1, series2)
    sumtab = crosstab.apply(lambda x: x / x.sum(), axis=1)
    pmi = np.log(sumtab) - np.log(sumtab.sum(axis=0))
    outliers = crosstab * np.where(np.abs(pmi) > 2, 1, 0)
    return np.sum(np.sum(outliers.to_numpy().flatten())) / len(series1)


# QQ
def get_correlation_qq(series1: pd.Series, series2: pd.Series) -> float:
    return series1.corr(series2)


def get_outlierness_qq(series1: pd.Series, series2: pd.Series) -> float:
    # use lof
    lof = LocalOutlierFactor()
    scores = lof.fit_predict(pd.concat([series1, series2], axis=1))
    return np.count_nonzero(scores == -1) / len(scores)


## QN
def get_correlation_qn(q_series: pd.Series, n_series: pd.Series) -> float:
    # logistic regression
    model = LogisticRegression(solver="lbfgs")
    model.fit(q_series, n_series)
    pred = model.predict(q_series)
    residuals = pred - n_series
    return np.corrcoef(residuals, pred)[0, 1]


def get_outlierness_qn(q_series: pd.Series, n_series: pd.Series) -> float:
    # use lof, encode n_series one-hot
    encoder = OneHotEncoder()
    n_train = encoder.fit_transform(n_series)
    lof = LocalOutlierFactor()
    scores = lof.fit_predict(pd.concat([q_series, n_train], axis=1))
    return np.count_nonzero(scores == -1) / len(scores)


def get_interestingness_from_nodes(
    nodes: list["VisualizationNode"], df: pd.DataFrame
) -> float:
    return 1.0
