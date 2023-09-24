import json
from waltzboard.model import ChartTokens


def tokenize(key: str) -> ChartTokens:
    tokens: list[str] = json.loads(key)
    return tuple(tokens)
