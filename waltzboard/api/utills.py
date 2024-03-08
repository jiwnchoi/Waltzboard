import json
from datetime import datetime
from typing import Literal

from waltzboard.model import ChartTokens


def tokenize(key: str) -> ChartTokens:
    tokens: list[str] = json.loads(key)
    return tuple(tokens)  # type: ignore


def getDateNow() -> str:
    return datetime.now().strftime("%H:%M:%S")


def printLog(
    type: Literal["REQ", "RES", "ERR"],
    endpoint: str,
    data,
):
    print(
        json.dumps(
            {
                "time": getDateNow(),
                "type": type,
                "endpoint": endpoint,
                "data": data,
            }
        )
    )
