from typing import Literal, TYPE_CHECKING
import pandas as pd

from gleaner.model import Attribute, ChartTokens, ChartSampled
from .chart_map import ChartMap
from itertools import product

if TYPE_CHECKING:
    from gleaner.model import BaseChart
    from gleaner.config import GleanerConfig


chart_hash: dict[ChartTokens, "BaseChart"] = {}


def get_chart_from_tokens(
    key: ChartTokens, config: "GleanerConfig"
) -> "BaseChart":
    name_type_map = {a.name: a.type for a in config.attrs}
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


def is_valid_tokens(key: ChartTokens, config: "GleanerConfig") -> bool:
    name_type_map = {a.name: a.type for a in config.attrs}
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


def get_chart_from_sample(
    sample: ChartSampled, df: pd.DataFrame
) -> "BaseChart":
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
    charts: "BaseChart", config: "GleanerConfig"
) -> list["BaseChart"]:
    variants = []
    for c in config.chart_type:
        if c != charts.tokens[0]:
            new_key = (c, *charts.tokens[1:])
            if is_valid_tokens(new_key, config):
                variants.append(get_chart_from_tokens(new_key, config))

    for i, attr in enumerate(config.attrs):
        for j in range(1, 4):
            if attr.name != charts.tokens[j]:
                new_key = (
                    charts.tokens[0],
                    *charts.tokens[1:j],
                    attr.name,
                    *charts.tokens[j + 1 :],
                )
                if is_valid_tokens(new_key, config):
                    variants.append(get_chart_from_tokens(new_key, config))
    for c, tx, ty, tz in product(
        config.chart_type, config.txs, config.tys, config.tzs
    ):
        if (
            c != charts.tokens[0]
            and tx != charts.tokens[4]
            and ty != charts.tokens[5]
            and tz != charts.tokens[6]
        ):
            new_key = (
                c,
                charts.tokens[1],
                charts.tokens[2],
                charts.tokens[3],
                tx,
                ty,
                tz,
            )
            if is_valid_tokens(new_key, config):
                variants.append(get_chart_from_tokens(new_key, config))
    return variants


def get_all_charts(config: "GleanerConfig") -> list["BaseChart"]:
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
