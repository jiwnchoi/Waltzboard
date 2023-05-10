import numpy as np
from scipy import stats


def f_oneway(category: np.ndarray, numerical: np.ndarray):
    grand_mean = np.mean(numerical)
    groups = np.unique(category)

    # between group sum of squares
    ssb = 0
    for group in groups:
        group_mean = np.mean(numerical[category == group])
        ssb += (group_mean - grand_mean) ** 2

    # within group sum of squares
    ssw = 0
    for group in groups:
        group_mean = np.mean(numerical[category == group])
        ssw += np.sum((numerical[category == group] - group_mean) ** 2)

    # degrees of freedom
    dfb = len(groups) - 1
    dfw = len(category) - len(groups)

    # mean square
    msb = ssb / dfb
    msw = ssw / dfw

    # f-statistic
    f_statistic = msb / msw
    # p-value
    p_value = 1 - stats.f.cdf(f_statistic, dfb, dfw)
    return f_statistic, p_value
