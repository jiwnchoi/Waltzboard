from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from math import ceil
from os import cpu_count
from random import sample
from typing import Literal, Any
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
class SequenceScores:
    score: list[float]
    coverage: list[float]
    uniqueness: list[float]
    interestingness: list[float]
    specificity: list[float]

    def to_dict(self):
        return {
            "score": self.score,
            "coverage": self.coverage,
            "uniqueness": self.uniqueness,
            "interestingness": self.interestingness,
            "specificity": self.specificity,
        }


@dataclass
class ColumbusCofnig:
    max_attributes: int = 3
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
    oracle_weight: OracleWeight

    sampled_results: list[OracleResult]
    sampled_sequences: list[list[VisualizationNode]]

    max_sequence_idx: int
    statistic_features: list[dict[str, list[str | None]]]

    def get_max_sequence(self) -> list[VisualizationNode]:
        return self.sampled_sequences[self.max_sequence_idx]

    def get_max_result(self) -> OracleResult:
        return self.sampled_results[self.max_sequence_idx]

    def get_multiview(self, num_columns: int) -> alt.VConcatChart:
        altairs = [
            node.get_altair().properties(width=100, height=100)
            for node in self.get_max_sequence()
        ]
        rows: list[alt.HConcatChart] = [
            alt.hconcat(*altairs[i : i + num_columns]).resolve_scale(
                color="independent"
            )
            for i in range(0, len(self.get_max_sequence()), num_columns)
        ]
        return alt.vconcat(*rows)

    def get_info(self) -> str:
        return f"Score\n\n{self.get_max_result().get_score()}\n\nOracle Result\n\n{self.get_max_result()}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "indices": [node.index for node in self.get_max_sequence()],
            "vlspecs": [node.get_vegalite() for node in self.get_max_sequence()],
            "statistic_features": self.statistic_features,
            "sampled_results": [result.to_dict() for result in self.sampled_results],
            "result": self.get_max_result().to_dict(),
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
        list(comb)
        for i in range(0, config.max_filters + 1)
        for comb in combinations(single_filters, i)
    ]

    print(len(filter_combinations))

    colum_combinations = [
        list(comb)
        for i in range(1, config.max_attributes + 1)
        for comb in combinations(columns.values(), i)
    ]

    filtered_dfs: list[VisualizableDataFrame] = []

    for filter_comb in filter_combinations:
        column_filter = {}
        if len(filter_comb) == 0:
            filtered_dfs.append(VisualizableDataFrame(df, [], None))
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
            filtered_dfs.append(VisualizableDataFrame(tmp_df, [], filter_comb))

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
                index=-1,
                sub_df=sub_df.df,
                attrs=sub_df.attrs,
                filters=sub_df.filter,
                binnings=None,
                aggregation=None,
                encoding=None,
            )
            for sub_df in self.sub_dfs
        ]
        self.visualizations: list[VisualizationNode] = []
        for node in self.nodes:
            self.visualizations.extend(node.get_children())

        for index, node in enumerate(self.visualizations):
            node.index = index

    def __len__(self) -> int:
        return len(self.visualizations)

    def infer(self, oracle: ColumbusOracle, indices: list[int]) -> float:
        target = [self.visualizations[i] for i in indices]
        result = oracle.get_result(target, self.df, set(), self.statistical_features)
        return float(result.get_score())

    def sample(
        self,
        indices: list[int],
        oracle: ColumbusOracle,
        num_views: int,
        num_samples: int,
        num_filters: int,
        wildcards: list[str],
        targetChartType: list[str],
    ):
        subspace = [
            s
            for s in self.visualizations
            if s.encoding and s.encoding.chart_type in targetChartType
            if s.filters is None or (s.filters and len(s.filters) <= num_filters)
            if s.index not in indices
        ]

        current_chart = [self.visualizations[i] for i in indices]

        num_samples = min(num_samples, len(subspace))
        num_additional_charts = num_views - len(indices)

        sampled_sequences = [
            current_chart + list(sample(subspace, num_additional_charts))
            for _ in range(num_samples)
        ]

        sampled_results = [
            oracle.get_result(
                multiview, self.df, set(wildcards), self.statistical_features
            )
            for multiview in sampled_sequences
        ]

        sampled_scores = SequenceScores(
            score=[result.get_score() for result in sampled_results],
            coverage=[result.coverage for result in sampled_results],
            uniqueness=[result.uniqueness for result in sampled_results],
            specificity=[result.specificity for result in sampled_results],
            interestingness=[result.interestingness for result in sampled_results],
        )
        max_score = max(sampled_scores.score)
        idx = sampled_scores.score.index(max_score)

        result = sampled_results[idx]
        sequence = sampled_sequences[idx]
        statistic_features = [
            oracle.get_statistic_features(node, self.statistical_features)
            for node in sequence
        ]

        return Multiview(
            oracle_weight=result.weight,
            sampled_results=sampled_results,
            sampled_sequences=sampled_sequences,
            max_sequence_idx=idx,
            statistic_features=statistic_features,
        )

    def get_attributes(self) -> list[dict[str, str]]:
        return [col.to_dict() for col in self.columns.values()]

    def get_config(self) -> dict[str, int]:
        return self.config.to_dict()
