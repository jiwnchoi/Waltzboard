from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from ..space.Node import VISNode


def get_interestingness_from_nodes(nodes: list["VISNode"], df: pd.DataFrame) -> float:
    return 1.0
