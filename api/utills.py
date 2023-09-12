import json
from gleaner.model import ChartTokens


def tokenize(key: str) -> ChartTokens:
    tokens: list[str] = json.loads(key)
    return tuple(tokens)
