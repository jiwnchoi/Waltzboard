from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..space.Node import VISNode


def includeness(bovs: set, wildcard: set) -> float:
    return len(bovs.intersection(wildcard)) / len(wildcard)


def get_specificity_from_nodes(nodes: list["VISNode"], wildcard: set[str]) -> float:
    bovs = [node.get_bov() for node in nodes]
    specificities = [includeness(bov, wildcard) for bov in bovs]
    return sum(specificities) / len(specificities)
