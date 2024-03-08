from __future__ import annotations

import json
import pathlib

from pydantic import BaseModel

from waltzboard.model import BaseChart
from waltzboard.oracle import OracleResult, Statistics

# i18n

locales = json.load(
    open(pathlib.Path(__file__).parent.parent.parent / "locales/default.json")
)


class OracleWeightModel(BaseModel):
    specificity: float
    interestingness: float
    diversity: float
    coverage: float
    parsimony: float


class OracleResultModel(BaseModel):
    score: float
    specificity: float
    interestingness: float
    diversity: float
    coverage: float
    parsimony: float

    @staticmethod
    def from_oracle_result(res: OracleResult):
        return OracleResultModel(
            score=res.get_score(),
            specificity=res.specificity,
            interestingness=res.interestingness,
            diversity=res.diversity,
            coverage=res.coverage,
            parsimony=res.parsimony,
        )


class ChartTypeModel(BaseModel):
    name: str
    mark: str


class TaskTypeModel(BaseModel):
    name: str
    weight: OracleWeightModel
    chartTypes: list["ChartTypeModel"]


class TrsTypeModel(BaseModel):
    name: str
    type: str | None


class AttributeModel(BaseModel):
    name: str
    type: str


class AttributeDistModel(BaseModel):
    name: str
    x: float
    y: float
    z: float


class ChartTypeDistModel(BaseModel):
    name: str
    prob: float


class TransformationDistModel(BaseModel):
    name: str
    x: float
    y: float
    z: float


class WaltzboardChartModel(BaseModel):
    key: str
    spec: str
    title: list[str]
    statistics: list[dict[str, str | list[str | None]]]

    @staticmethod
    def from_waltzboard_chart(chart: BaseChart, statistics: list[Statistics] = []):
        return WaltzboardChartModel(
            key=json.dumps(chart.tokens),
            spec=chart.get_vegalite(),
            title=chart.title_tokens,
            statistics=[s.to_dict() for s in statistics],
        )


class ScoreDistModel(BaseModel):
    score: list[float]
    specificity: list[float]
    interestingness: list[float]
    diversity: list[float]
    coverage: list[float]
    parsimony: list[float]


class SetConfigBody(BaseModel):
    nCandidates: int
    nFilters: int
    robustness: int
    halvingRatio: float


chart_types: dict[str, ChartTypeModel] = {
    "bar": ChartTypeModel(name=locales["token-bar"], mark="bar"),
    "line": ChartTypeModel(name=locales["token-line"], mark="line"),
    "pie": ChartTypeModel(name=locales["token-pie"], mark="arc"),
    "scatter": ChartTypeModel(name=locales["token-point"], mark="point"),
    "heatmap": ChartTypeModel(name=locales["token-rect"], mark="rect"),
    "boxplot": ChartTypeModel(name=locales["token-boxplot"], mark="boxplot"),
    "stripplot": ChartTypeModel(name=locales["token-tick"], mark="tick"),
}

# Count, Mean, Sum, Min, Max
trs_types: dict[str, TrsTypeModel] = {
    "none": TrsTypeModel(name=locales["token-none"], type=None),
    "count": TrsTypeModel(name=locales["token-count"], type="count"),
    "mean": TrsTypeModel(name=locales["token-mean"], type="mean"),
    "sum": TrsTypeModel(name=locales["token-sum"], type="sum"),
    "min": TrsTypeModel(name=locales["token-min"], type="min"),
    "max": TrsTypeModel(name=locales["token-max"], type="max"),
    "bin": TrsTypeModel(name=locales["token-bin"], type="bin"),
    "year": TrsTypeModel(name=locales["token-year"], type="year"),
    "month": TrsTypeModel(name=locales["token-month"], type="month"),
    "day": TrsTypeModel(name=locales["token-day"], type="day"),
}
