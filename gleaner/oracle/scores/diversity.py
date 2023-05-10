import numpy as np
from gleaner.model import GleanerChart


def jcd_index(sets: list[set], preferences: set[str]) -> float:
    n = len(sets)
    intersections = [
        set1.intersection(set2) - preferences for i, set1 in enumerate(sets) for j, set2 in enumerate(sets) if i < j
    ]
    unions = [set1.union(set2) for i, set1 in enumerate(sets) for j, set2 in enumerate(sets) if i < j]
    jaccard_matrix = np.zeros((n, n))
    jaccard_matrix[np.triu_indices(n, 1)] = 1 - np.array(list(map(len, intersections))) / np.array(
        list(map(len, unions))
    )
    return jaccard_matrix[np.triu_indices(n, 1)].sum() - n


def get_diversity_from_nodes(nodes: list["GleanerChart"], preferences: set[str]) -> float:
    bovs = [node.get_bov() for node in nodes]
    n = len(bovs)
    return jcd_index(bovs, preferences) / (n * (n - 1) / 2)
