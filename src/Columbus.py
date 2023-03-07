from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from math import ceil
from os import cpu_count
from random import sample
from typing import Literal
import altair as alt
import pandas as pd
from pathos.multiprocessing import ProcessingPool as Pool

from .oracle import ColumbusOracle, OracleResult, OracleWeight
from .oracle.Interestingness import get_statistic_feature_hashmap
from .space.DataModel import Attribute, VisualizableDataFrame
from .space.Node import VisualizationNode, chart_type

agg_types: list[str] = ["max", "min", "mean", "sum"]
EncodingType = Literal["bar", "line", "area", "pie", "scatter", "box", "heatmap"]


@dataclass
class ColumbusCofnig:
    max_attributes: int = 4
    max_categories: int = 10
    max_filters: int = 1
    min_rows: int = 4

    def to_dict(self):
        return {
            "max_attributes": self.max_attributes,
            "max_categories": self.max_categories,
            "max_filters": self.max_filters,
            "min_rows": self.min_rows,
        }


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
            node.get_altair().properties(width=100, height=100)
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

    def to_dict(self) -> dict:
        return {
            "num_views": self.num_views,
            "wildcards": self.wildcards,
            "score": self.score,
            "oracle_result": self.oracle_result.to_dict(),
            "oracle_weight": self.oracle_weight.to_dict(),
            "vlspecs": [node.get_vegalite() for node in self.chart_sequence],
        }


def get_sub_dfs(
    df: pd.DataFrame, columns: dict[str, "Attribute"], config: ColumbusCofnig
) -> list[list[VisualizableDataFrame]]:
    single_filters = [
        (col, value, df[col] == value)
        for col in columns
        if columns[col].type == "C" and df[col].nunique() < config.max_categories
        for value in df[col].unique()
    ]

    filter_combinations = [
        tuple(comb)
        for i in range(0, config.max_filters + 1)
        for comb in combinations(single_filters, i)
    ]

    print(len(filter_combinations))

    colum_combinations = [
        tuple(comb)
        for i in range(1, config.max_attributes + 1)
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
        if len(tmp_df) >= config.min_rows:
            filtered_dfs.append(VisualizableDataFrame(tmp_df, (), filter_comb))

    return [
        [
            VisualizableDataFrame(
                filtered_df.df[[col.name for col in comb]], comb, filtered_df.filter
            )
            for comb in colum_combinations
        ]
        for filtered_df in filtered_dfs
    ]


def split_list(lst, num_chunks):
    chunk_size = ceil(len(lst) / num_chunks)
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_type(series: pd.Series):
    if series.dtype == "object" and series.nunique() <= 10:
        return "C"
    elif series.dtype == "object" and series.nunique() > 10:
        return "N"
    else:
        return "Q"


class Columbus:
    def __init__(self, df: pd.DataFrame, config: ColumbusCofnig) -> None:
        self.columns: dict[str, Attribute] = {
            col: Attribute(col, get_type(df[col]))
            for col in [str(col) for col in df.columns]
        }
        self.df = df[[col.name for col in self.columns.values() if col.type != "N"]]

        sub_dfs_by_filter = get_sub_dfs(df, self.columns, config)
        self.sub_dfs = [item for sublist in sub_dfs_by_filter for item in sublist]

        self.statistical_features = {}
        self.config = config

        outputs: list[dict] = []

        if self.config.max_filters == 0:
            outputs: list[dict] = [get_statistic_feature_hashmap(self.sub_dfs)]
            self.statistical_features = outputs[0]
        else:
            pool = Pool(cpu_count())
            outputs: list[dict] = pool.map(
                get_statistic_feature_hashmap, sub_dfs_by_filter
            )
            self.statistical_features = {
                key: value for output in outputs for key, value in output.items()
            }

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

    def sample(
        self,
        oracle: ColumbusOracle,
        num_views: int,
        num_samples: int,
        wildcards: list[str],
        targetChartType: list[str],
    ) -> "Multiview":
        subspace = [
            s
            for s in self.visualizations
            if s.encoding and s.encoding.chart_type in targetChartType
        ]
        samples = [sample(subspace, num_views) for _ in range(num_samples)]

        multiview_oracle_result = [
            oracle.get_result(
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
            oracle_weight=oracle.weight,
            chart_sequence=sample_sequence,
        )

    def get_attributes(self) -> list[dict[str, str]]:
        return [col.to_dict() for col in self.columns.values()]

    def get_config(self) -> dict[str, int]:
        return self.config.to_dict()
