import json
import altair as alt
from pydantic import BaseModel
from gleaner.model import GleanerChart
from gleaner.oracle import OracleResult

# Atoms


class OracleWeightModel(BaseModel):
    specificity: float
    interestingness: float
    diversity: float
    coverage: float
    conciseness: float


class OracleResultModel(BaseModel):
    score: float
    specificity: float
    interestingness: float
    diversity: float
    coverage: float
    conciseness: float

    @staticmethod
    def from_oracle_result(res: OracleResult):
        return OracleResultModel(
            score=res.get_score(),
            specificity=res.specificity,
            interestingness=res.interestingness,
            diversity=res.diversity,
            coverage=res.coverage,
            conciseness=res.conciseness,
        )


class ChartTypeModel(BaseModel):
    name: str
    mark: str


class TaskTypeModel(BaseModel):
    name: str
    weight: OracleWeightModel
    chartTypes: list["ChartTypeModel"]


class AttributeModel(BaseModel):
    name: str
    type: str


class GleanerChartModel(BaseModel):
    key: str
    spec: str
    title: list[str]
    statistics: dict[str, list[str | None]]

    @staticmethod
    def from_gleaner_chart(chart: GleanerChart, statistics: dict[str, list[str | None]] = {}):
        return GleanerChartModel(
            key=chart.key,
            spec=chart.get_vegalite(),
            title=chart.title_tokens,
            statistics=statistics,
        )


class ScoreDistModel(BaseModel):
    score: list[float]
    specificity: list[float]
    interestingness: list[float]
    diversity: list[float]
    coverage: list[float]
    conciseness: list[float]


# Bodys


class InferBody(BaseModel):
    nCharts: int | None
    chartKeys: list[str]


class TrainBody(BaseModel):
    weight: OracleWeightModel
    preferences: list[str]
    constraints: list[str]


class RecommendBody(BaseModel):
    chartKeys: list[str]
    nResults: int


class SetConfigBody(BaseModel):
    nCandidates: int
    nFilters: int
    robustness: int
    halvingRatio: float


class ScoreBody(BaseModel):
    chartKeys: list[str]


# Responses


class InitResponse(BaseModel):
    chartTypes: list[ChartTypeModel]
    taskTypes: list[TaskTypeModel]
    attributes: list[AttributeModel]


class InferResponse(BaseModel):
    charts: list[GleanerChartModel]
    result: OracleResultModel
    dist: ScoreDistModel


class RecommendResponse(BaseModel):
    charts: list[GleanerChartModel]


class ScoreResponse(BaseModel):
    result: OracleResultModel


chart_types: dict[str, ChartTypeModel] = {
    "bar": ChartTypeModel(name="Bar Chart", mark="bar"),
    "line": ChartTypeModel(name="Line Chart", mark="line"),
    "pie": ChartTypeModel(name="Pie Chart", mark="pie"),
    "scatter": ChartTypeModel(name="Scatterplot", mark="point"),
    "area": ChartTypeModel(name="Area Chart", mark="area"),
    "heatmap": ChartTypeModel(name="Heatmap", mark="rect"),
    "boxplot": ChartTypeModel(name="Boxplot", mark="boxplot"),
    "stripplot": ChartTypeModel(name="Strip Plot", mark="tick"),
}


task_types: dict[str, TaskTypeModel] = {
    "retrieve": TaskTypeModel(
        name="Retrieve Value",
        weight=OracleWeightModel(coverage=2, diversity=0, specificity=2, interestingness=0, conciseness=1),
        chartTypes=[chart_types["scatter"], chart_types["heatmap"]],
    ),
    "correlation": TaskTypeModel(
        name="Correlation",
        weight=OracleWeightModel(coverage=0, diversity=2, specificity=1, interestingness=2, conciseness=1),
        chartTypes=[chart_types["scatter"], chart_types["heatmap"]],
    ),
    "compare": TaskTypeModel(
        name="Compare",
        weight=OracleWeightModel(coverage=0, diversity=2, specificity=2, interestingness=0, conciseness=1),
        chartTypes=[
            chart_types["bar"],
            chart_types["line"],
            chart_types["area"],
            chart_types["scatter"],
            chart_types["heatmap"],
        ],
    ),
    "cluster": TaskTypeModel(
        name="Cluster",
        weight=OracleWeightModel(coverage=1, diversity=1, specificity=1, interestingness=-3, conciseness=1),
        chartTypes=[chart_types["scatter"], chart_types["heatmap"]],
    ),
    "distribution": TaskTypeModel(
        name="Characterize Distribution",
        weight=OracleWeightModel(coverage=2, diversity=2, specificity=1, interestingness=0, conciseness=1),
        chartTypes=[
            chart_types["scatter"],
            chart_types["boxplot"],
            chart_types["stripplot"],
            chart_types["bar"],
            chart_types["line"],
            chart_types["area"],
            chart_types["heatmap"],
        ],
    ),
    "anomalies": TaskTypeModel(
        name="Find Anomalies",
        weight=OracleWeightModel(coverage=1, diversity=1, specificity=1, interestingness=2, conciseness=1),
        chartTypes=[
            chart_types["scatter"],
            chart_types["line"],
            chart_types["boxplot"],
            chart_types["heatmap"],
            chart_types["stripplot"],
        ],
    ),
    "extremum": TaskTypeModel(
        name="Find Extremum",
        weight=OracleWeightModel(coverage=1, diversity=1, specificity=1, interestingness=0, conciseness=1),
        chartTypes=[chart_types["bar"], chart_types["line"], chart_types["scatter"]],
    ),
    "derived": TaskTypeModel(
        name="Compute Derived Value",
        weight=OracleWeightModel(coverage=1, diversity=2, specificity=2, interestingness=1, conciseness=1),
        chartTypes=[chart_types["bar"], chart_types["line"], chart_types["scatter"], chart_types["pie"]],
    ),
}
