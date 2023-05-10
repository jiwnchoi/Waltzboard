from gleaner.model import GleanerChart


def includeness(bovs: set, preferences: set) -> float:
    return len(bovs.intersection(preferences)) / len(preferences)


def get_specificity_from_nodes(nodes: list["GleanerChart"], preferences: set[str]) -> float:
    if len(preferences) == 0:
        return 0.0

    bovs = [node.get_bov() for node in nodes]
    specificities = [includeness(bov, preferences) for bov in bovs]
    return sum(specificities) / len(specificities)
