from gleaner.model import BaseChart


def includeness(bovs: set, preferences: set) -> float:
    return len(bovs.intersection(preferences)) / len(preferences)


def get_specificity_from_nodes(nodes: list["BaseChart"], preferences: set[str]) -> float:
    if len(preferences) == 0:
        return 0.0

    bots = [node.get_bot() for node in nodes]
    specificities = [includeness(bot, preferences) for bot in bots]
    if len(specificities) == 0:
        return 0.0
    return sum(specificities) / len(specificities)
