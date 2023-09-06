from typing import Literal, TYPE_CHECKING
import pandas as pd

from gleaner.model import Attribute, ChartTokens, ChartSampled
from .chart_map import ChartMap


if TYPE_CHECKING:
    from gleaner.model import BaseChart


chart_hash: dict[ChartTokens, "BaseChart"] = {}


def get_chart_from_tokens(key: ChartTokens, df: pd.DataFrame) -> "BaseChart":
    chart = chart_hash.get(key)
    return chart if chart else ChartMap[key](key, df)


def get_chart_from_sample(sample: ChartSampled, df: pd.DataFrame) -> "BaseChart":
    if not (sample[0] and sample[1].name):
        raise Exception("Chart sample is not valid")
    chart_tokens = (
        sample[0],
        sample[1].name,
        sample[2].name,
        sample[3].name,
        sample[4],
        sample[5],
        sample[6],
    )
    chart_key_tokens = (
        sample[0],
        sample[1].type,
        sample[2].type,
        sample[3].type,
        sample[4],
        sample[5],
        sample[6],
    )
    chart = chart_hash.get(chart_tokens)  # type: ignore
    if not chart:
        chart = ChartMap[chart_key_tokens](sample, df)
        chart_hash[chart_tokens] = chart
    return chart
