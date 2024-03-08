from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from waltzboard.model import BaseChart


def jcd_index(sets: list[set], preferences: set[str]) -> float:
    n = len(sets)
    if n < 2:
        print(n)
    return sum(
        [
            (
                1
                - (len(set1.intersection(set2) - preferences) + 1e-10)
                / (len(set1.union(set2)) + 1e-10)
            )
            for i, set1 in enumerate(sets)
            for j, set2 in enumerate(sets)
            if i < j
        ]
    ) / (n * (n - 1) / 2)


def new_div(sets: list[set], preferences: set[str]) -> float:
    all_unions = len(set.union(*sets))
    all_tokens = sum([len(s) for s in sets])
    return (all_unions / all_tokens) if all_tokens else 1.0


def get_diversity(nodes: list["BaseChart"], preferences: set[str]) -> float:
    bots = [node.get_bot() for node in nodes]
    if len(nodes) == 1 or len(nodes) == 0:
        return 1.0
    return new_div(bots, preferences)


def get_diversity_old(nodes: list["BaseChart"], preferences: set[str]) -> float:
    bots = [node.get_bot() for node in nodes]
    if len(nodes) == 1 or len(nodes) == 0:
        return 1.0

    idx = jcd_index(bots, preferences)

    if np.isnan(idx / (len(nodes) * (len(nodes) - 1) / 2)):
        return idx
    return idx / (len(nodes) * (len(nodes) - 1) / 2)
