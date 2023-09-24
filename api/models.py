import json
import altair as alt
from pydantic import BaseModel
from waltzboard.model import BaseChart, ChartTokens
from waltzboard.oracle import OracleResult, OracleSingleResult, Statistics


# Atoms


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


class OracleSingleResultModel(BaseModel):
    score: float
    specificity: float
    interestingness: float
    diversity: float
    coverage: float

    @staticmethod
    def from_oracle_result(res: OracleSingleResult):
        return OracleSingleResultModel(
            score=res.get_score(),
            specificity=res.specificity,
            interestingness=res.interestingness,
            diversity=res.diversity,
            coverage=res.coverage,
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
    "bar": ChartTypeModel(name="Bar Chart", mark="bar"),
    "line": ChartTypeModel(name="Line Chart", mark="line"),
    "pie": ChartTypeModel(name="Pie Chart", mark="arc"),
    "scatter": ChartTypeModel(name="Scatter Plot", mark="point"),
    "heatmap": ChartTypeModel(name="Heatmap", mark="rect"),
    "boxplot": ChartTypeModel(name="Box Plot", mark="boxplot"),
    "stripplot": ChartTypeModel(name="Strip Plot", mark="tick"),
}

# Count, Mean, Sum, Min, Max
trs_types: dict[str, TrsTypeModel] = {
    "none": TrsTypeModel(name="None", type=None),
    "count": TrsTypeModel(name="Count", type="count"),
    "mean": TrsTypeModel(name="Mean", type="mean"),
    "sum": TrsTypeModel(name="Sum", type="sum"),
    "min": TrsTypeModel(name="Min", type="min"),
    "max": TrsTypeModel(name="Max", type="max"),
    "bin": TrsTypeModel(name="Bin", type="bin"),
    "year": TrsTypeModel(name="Year", type="year"),
    "month": TrsTypeModel(name="Month", type="month"),
    "day": TrsTypeModel(name="Day", type="day"),
}
