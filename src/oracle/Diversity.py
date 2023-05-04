from typing import TYPE_CHECKING
import numpy as np


if TYPE_CHECKING:
    from ..space.Node import VisualizationNode
    from ..space.Node import VisualizationNode


def jcd_index(sets: list[set]) -> float:
    n = len(sets)
    intersections = [
        set1.intersection(set2)
        for i, set1 in enumerate(sets)
        for j, set2 in enumerate(sets)
        if i < j
    ]
    unions = [
        set1.union(set2)
        for i, set1 in enumerate(sets)
        for j, set2 in enumerate(sets)
        if i < j
    ]
    jaccard_matrix = np.zeros((n, n))
    jaccard_matrix[np.triu_indices(n, 1)] = 1 - np.array(
        list(map(len, intersections))
    ) / np.array(list(map(len, unions)))
    return jaccard_matrix[np.triu_indices(n, 1)].sum() - n


def get_diversity_from_nodes(
    nodes: list["VisualizationNode"],
) -> float:
    bovs = [node.get_bov() for node in nodes]
    n = len(bovs)
    return jcd_index(bovs) / (n * (n - 1) / 2)
