import pandas as pd
from gleaner.model import GleanerChart


def get_coverage_from_nodes(nodes: list["GleanerChart"], df: pd.DataFrame) -> float:
    n = len(nodes)
    coverages = [node.get_coverage(df) for node in nodes]
    full_coverage = {key: 0.0 for key in list(df.columns)}
    for coverage in coverages:
        for key, value in coverage.items():
            full_coverage[key] = min(1, full_coverage[key] + value)
    return sum(full_coverage.values()) / (len(full_coverage))
