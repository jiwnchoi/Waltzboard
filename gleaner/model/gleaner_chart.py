from typing import Literal, TYPE_CHECKING
import pandas as pd

from gleaner.model import Attribute, ChartTokens, ChartSampled
from .chart_map import ChartMap


if TYPE_CHECKING:
    from gleaner.model import BaseChart
    from gleaner.config import GleanerConfig


chart_hash: dict[ChartTokens, "BaseChart"] = {}


def get_chart_from_tokens(key: ChartTokens, config: "GleanerConfig") -> "BaseChart":
    name_type_map = {a.name: a.type for a in config.attrs}
    print(name_type_map)
    type_key = (
        key[0],
        name_type_map[key[1]],
        name_type_map[key[2]],
        name_type_map[key[3]],
        key[4],
        key[5],
        key[6],
    )
    chart = chart_hash.get(key)
    return chart if chart else ChartMap[key](type_key, config.df)


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
