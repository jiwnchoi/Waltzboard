from typing import TYPE_CHECKING

import pandas as pd

from .attribute import Attribute
from .chart_map import ChartMap
from .const import ChartSampled, ChartTokens

if TYPE_CHECKING:
    from waltzboard.config import WaltzboardConfig

    from .charts import BaseChart


chart_hash: dict[ChartTokens, "BaseChart"] = {}


def get_chart_from_tokens(key: ChartTokens, config: "WaltzboardConfig") -> "BaseChart":
    name_type_map = {a.name: a.type for a in config.raw_attrs}
    type_key = (
        key[0],
        name_type_map[key[1]],
        name_type_map[key[2]],
        name_type_map[key[3]],
        key[4],
        key[5],
        key[6],
    )
    sampled = (
        key[0],
        Attribute(key[1], name_type_map[key[1]]),
        Attribute(key[2], name_type_map[key[2]]),
        Attribute(key[3], name_type_map[key[3]]),
        key[4],
        key[5],
        key[6],
    )
    chart = chart_hash.get(key)
    return chart if chart else ChartMap[type_key](sampled, config.df)


def is_valid_tokens(key: ChartTokens, config: "WaltzboardConfig") -> bool:
    name_type_map = {a.name: a.type for a in config.raw_attrs}
    type_key = (
        key[0],
        name_type_map[key[1]],
        name_type_map[key[2]],
        name_type_map[key[3]],
        key[4],
        key[5],
        key[6],
    )
    if not ChartMap.get(type_key):
        return False

    not_none_attrs = [k for k in key[1:4] if k]
    if len(not_none_attrs) != len(set(not_none_attrs)):
        return False

    return True


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


def get_variants_from_charts(
    charts: "BaseChart", config: "WaltzboardConfig"
) -> list["BaseChart"]:
    variants = []
    for new_chart in config.all_charts:
        new_token = new_chart.tokens
        current_token = charts.tokens
        if current_token == new_token:
            continue

        diff_new_token = (
            new_token[0],
            new_token[1],
            new_token[2],
            new_token[3],
            str(new_token[4:]),
        )

        current_new_token = (
            current_token[0],
            current_token[1],
            current_token[2],
            current_token[3],
            str(current_token[4:]),
        )

        if (
            sum([1 if x != y else 0 for x, y in zip(diff_new_token, current_new_token)])
            == 1
        ):
            variants.append(new_chart)

    return variants


def get_all_charts(config: "WaltzboardConfig") -> list["BaseChart"]:
    all_charts = []
    typename = {
        "Q": [a.name for a in config.attrs if a.type == "Q"],
        "N": [a.name for a in config.attrs if a.type == "N"],
        "T": [a.name for a in config.attrs if a.type == "T"],
        None: [None],
    }
    chart_map = config.get_chart_map()
    for map in chart_map:
        for x_name in typename[map[1]]:
            for y_name in typename[map[2]]:
                if y_name == x_name:
                    continue
                for z_name in typename[map[3]]:
                    if z_name == x_name or z_name == y_name:
                        continue

                    all_charts.append(
                        (
                            map[0],
                            x_name,
                            y_name,
                            z_name,
                            map[4],
                            map[5],
                            map[6],
                        )
                    )

    return [get_chart_from_tokens(k, config) for k in all_charts]


__all__ = [
    "get_chart_from_tokens",
    "is_valid_tokens",
    "get_chart_from_sample",
    "get_variants_from_charts",
    "get_all_charts",
]
