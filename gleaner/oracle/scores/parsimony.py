import numpy as np
import pandas as pd


def get_parsimony_from_nodes(nodes):
    return 2 - 2 / (1 + np.exp(-len(nodes) + 4) / 2)
