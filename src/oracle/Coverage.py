from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from ..space.Node import VISNode


def get_coverage_from_nodes(nodes: list["VISNode"], df: pd.DataFrame) -> float:
    coverages = [node.get_coverage() for node in nodes]
    full_coverage = {key: 0.0 for key in list(df.columns)}
    for coverage in coverages:
        for key, value in coverage.items():
            full_coverage[key] = min(1, full_coverage[key] + value)
    return sum(full_coverage.values()) / len(full_coverage)
