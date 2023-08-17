import numpy as np
import pandas as pd


NUM_MIN_CHART = 2


def get_parsimony_from_nodes(nodes, df: pd.DataFrame):
    return np.exp(-(1 / len(df.columns)) * (len(nodes) - NUM_MIN_CHART))
