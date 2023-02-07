from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..space.Node import VISNode


def jaccard_similarity(set1: set, set2: set) -> float:
    return len(set1.intersection(set2)) / len(set1.union(set2))


def get_specificity_from_nodes(nodes: list["VISNode"], wildcard: set[str]) -> float:
    bovs = [node.get_bov() for node in nodes]
    specificities = [jaccard_similarity(bov, wildcard) for bov in bovs]
    return sum(specificities) / len(specificities)
