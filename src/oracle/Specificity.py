from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..model.Node import VisualizationNode


def includeness(bovs: set, wildcard: set) -> float:
    return len(bovs.intersection(wildcard)) / len(wildcard)


def get_specificity_from_nodes(
    nodes: list["VisualizationNode"], wildcard: set[str]
) -> float:
    if len(wildcard) == 0:
        return 0.0

    bovs = [node.get_bov() for node in nodes]
    specificities = [includeness(bov, wildcard) for bov in bovs]
    return sum(specificities) / len(specificities)
