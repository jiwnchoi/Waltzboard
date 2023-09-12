import numpy as np
import pandas as pd
from gleaner.model import BaseChart

NUM_MIN_CHART = 2


def get_parsimony(nodes: list[BaseChart], attr_names: list[str]):
    return np.exp((1 / len(attr_names)) * (NUM_MIN_CHART - len(nodes)))
