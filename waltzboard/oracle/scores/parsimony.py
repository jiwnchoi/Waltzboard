from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from waltzboard.config import WaltzboardConfig
    from waltzboard.model import BaseChart


def get_parsimony(nodes: list["BaseChart"], config: "WaltzboardConfig"):
    return min(
        1,
        np.exp(
            (1 / (2 * len(config.attr_names) - 1)) * (config.n_min_charts - len(nodes))
        ),
    )
