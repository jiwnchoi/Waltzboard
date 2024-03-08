from waltzboard.model import BaseChart


def get_coverage(nodes: list["BaseChart"], attr_names: list[str]) -> float:
    coverages = [node.get_coverage() for node in nodes]
    full_coverage = {key: 0.0 for key in attr_names}
    for coverage in coverages:
        for key, value in coverage.items():
            full_coverage[key] = min(1.0, full_coverage[key] + value)
    return sum(full_coverage.values()) / (len(full_coverage))
