import numpy as np
from gleaner.model import BaseChart


def jcd_index(sets: list[set], preferences: set[str]) -> float:
    n = len(sets)
    intersections = [
        set1.intersection(set2) - preferences
        for i, set1 in enumerate(sets)
        for j, set2 in enumerate(sets)
        if i < j
    ]
    unions = [
        set1.union(set2) - preferences
        for i, set1 in enumerate(sets)
        for j, set2 in enumerate(sets)
        if i < j
    ]
    jaccard_matrix = np.zeros((n, n))
    jaccard_matrix[np.triu_indices(n, 1)] = 1 - np.array(
        list(map(len, intersections))
    ) / np.array(list(map(len, unions)))
    return jaccard_matrix[np.triu_indices(n, 1)].sum() - n


def jcd_distance(sets: list[set], preferences: set[str], target: int) -> float:
    n = len(sets)

    target_set = sets[target]
    intersections = np.array(
        [
            target_set.intersection(s) - preferences
            for i, s in enumerate(sets)
            if i != target
        ]
    )
    unions = np.array(
        [
            target_set.union(s) - preferences
            for i, s in enumerate(sets)
            if i != target
        ]
    )
    distances = 1 - np.array(list(map(len, intersections))) / np.array(
        list(map(len, unions))
    )
    return distances.sum() / (n - 1)


def get_diversity(nodes: list["BaseChart"], preferences: set[str]) -> float:
    bots = [node.get_bot() for node in nodes]
    n = len(nodes)
    if n == 1:
        return 1.0
    return jcd_index(bots, preferences) / (n * (n - 1) / 2)


def get_diversity_single(
    nodes: list["BaseChart"], preferences: set[str], target: int
) -> float:
    bots = [node.get_bot() for node in nodes]
    n = len(nodes)
    if n == 1:
        return 1.0
    return jcd_distance(bots, preferences, target)
