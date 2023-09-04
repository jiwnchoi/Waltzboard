import numpy as np
import pandas as pd


NUM_MIN_CHART = 2


def get_parsimony_from_nodes(nodes, attr_names: list[str]):
    return np.exp(-(1 / len(attr_names)) * (len(nodes) - NUM_MIN_CHART))
