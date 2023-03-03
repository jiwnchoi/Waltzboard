from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from random import sample
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

import altair as alt
import pandas as pd

from config import (
    FILTER_VALUE_THRESHOLD,
    MAX_NUM_FILTERS,
    MAX_TARGET_ATTRIBUTES,
    MIN_ROWS,
    AggregationType,
)

from .oracle import ColumbusOracle, OracleWeight
from .space.DataModel import Attribute, VisualizableDataFrame
from .space.DataTransformsModel import Filter
from .space.Node import VisualizationNode

from .oracle.OracleResult import OracleResult
from .oracle.OracleWeight import OracleWeight
from .oracle.Interestingness import get_statistic_feature_hashmap

agg_types: list[AggregationType] = ["max", "min", "mean", "sum"]


@dataclass
class Multiview:
    num_views: int
    wildcards: list[str]
    score: float
    oracle_result: OracleResult
    oracle_weight: OracleWeight
    chart_sequence: list[VisualizationNode]

    def get_multiview(self, num_columns: int) -> alt.VConcatChart:
        altairs = [
            node.get_chart().properties(width=100, height=100)
            for node in self.chart_sequence
        ]
        rows: list[alt.HConcatChart] = [
            alt.hconcat(*altairs[i : i + num_columns]).resolve_scale(
                color="independent"
            )
            for i in range(0, self.num_views, num_columns)
        ]
        return alt.vconcat(*rows)

    def get_info(self) -> str:
        return f"Score\n\n{self.score}\n\nOracle Result\n\n{self.oracle_result}"


def get_sub_dfs(
    df: pd.DataFrame, columns: dict[str, "Attribute"]
) -> list[VisualizableDataFrame]:
    dfs: list[VisualizableDataFrame] = []
    single_filters = [
        (col, value, df[col] == value)
        for col in columns
        if columns[col].type == "N" and df[col].nunique() < FILTER_VALUE_THRESHOLD
        for value in df[col].unique()
    ]

    filter_combinations = [
        tuple(comb)
        for i in range(0, MAX_NUM_FILTERS + 1)
        for comb in combinations(single_filters, i)
    ]

    print(len(filter_combinations))

    colum_combinations = [
        tuple(comb)
        for i in range(1, MAX_TARGET_ATTRIBUTES)
        for comb in combinations(columns.values(), i)
    ]

    filtered_dfs: list[VisualizableDataFrame] = []

    for filter_comb in filter_combinations:
        column_filter = {}
        if len(filter_comb) == 0:
            filtered_dfs.append(VisualizableDataFrame(df, (), None))
            continue

        for condition in filter_comb:
            column_name = condition[0]
            if column_name in column_filter:
                column_filter[column_name] = column_filter[column_name] | condition[2]
            else:
                column_filter[column_name] = condition[2]

        combined_filter = reduce(lambda x, y: x & y, column_filter.values())
        tmp_df = df[combined_filter]
        tmp_df = df.dropna()
        if len(tmp_df) >= MIN_ROWS:
            filtered_dfs.append(VisualizableDataFrame(tmp_df, (), filter_comb))

    dfs = [
        VisualizableDataFrame(
            filtered_df.df[[col.name for col in comb]], comb, filtered_df.filter
        )
        for filtered_df in filtered_dfs
        for comb in colum_combinations
    ]
    return dfs


class Columbus:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.columns: dict[str, Attribute] = {
            col: Attribute(col, ("N" if df[col].dtype == "object" else "Q"))
            for col in [str(col) for col in df.columns]
        }
        self.sub_dfs = get_sub_dfs(df, self.columns)

        self.statistical_features = get_statistic_feature_hashmap(self.sub_dfs)

        self.oracle = ColumbusOracle(OracleWeight())
        self.nodes = [
            VisualizationNode(
                sub_df=sub_df.df,
                attrs=sub_df.attrs,
                filters=sub_df.filter,
                binnings=None,
                aggregation=None,
                encoding=None,
                chart=None,
            )
            for sub_df in self.sub_dfs
        ]
        self.visualizations: list[VisualizationNode] = []
        for node in self.nodes:
            self.visualizations.extend(node.get_children())

    def __len__(self) -> int:
        return len(self.visualizations)

    def sample(self, num_views: int, wildcards: list[str]) -> "Multiview":
        samples = [sample(self.visualizations, num_views) for _ in range(10)]
        multiview_oracle_result = [
            self.oracle.get_result(
                multiview, self.df, set(wildcards), self.statistical_features
            )
            for multiview in samples
        ]
        multiview_scores = [result.get_score() for result in multiview_oracle_result]
        score = max(multiview_scores)
        idx = multiview_scores.index(max(multiview_scores))
        result = multiview_oracle_result[idx]
        sample_sequence = samples[idx]

        return Multiview(
            num_views=num_views,
            wildcards=wildcards,
            score=score,
            oracle_result=result,
            oracle_weight=self.oracle.weight,
            chart_sequence=sample_sequence,
        )
