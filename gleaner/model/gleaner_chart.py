import json
from ast import literal_eval
from typing import Literal, Optional, Set, Tuple, Union

import altair as alt
import pandas as pd

from gleaner.model import Attribute

from .attribute import AttrTypes
from .data_transforms import AggTypes, AggXTypes
from .charts import BaseChart
from .chart_map import ChartMap

MarkTypes = Literal["bar", "arc", "tick", "point", "rect", "line", "boxplot"]

AllTokenTypes = MarkTypes | AttrTypes | AggTypes | AggXTypes

ChartSampled = tuple[MarkTypes, Attribute, Attribute, Attribute, AggXTypes, AggTypes, AggTypes]
ChartTokens = tuple[MarkTypes, str, str | None, str | None, AggXTypes, AggTypes, AggTypes]
ChartKeyTokens = tuple[MarkTypes, AttrTypes, AttrTypes, AttrTypes, AggXTypes, AggTypes, AggTypes]

chart_hash: dict[ChartTokens, "BaseChart"] = {}


def get_gleaner_chart_from_key(key: ChartTokens) -> "BaseChart":
    chart = chart_hash.get(key)
    if not chart:
        raise Exception("Chart not found")
    return chart


def get_gleaner_chart(sample: ChartSampled, df: pd.DataFrame) -> "BaseChart":
    if sample[0] and sample[1].name:
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
    return chart if chart else ChartMap[chart_key_tokens](sample, df)
