from dataclasses import dataclass
from src.oracle import OracleWeight
from src.oracle.ChartType import ChartType, chart_types


@dataclass
class TaskType:
    name: str
    weight: OracleWeight
    chartTypes: list["ChartType"]

    def to_dict(self):
        return {
            "name": self.name,
            "weight": self.weight.to_dict(),
            "chartTypes": [chartType.to_dict() for chartType in self.chartTypes],
        }


task_types: dict[str, TaskType] = {
    "retrieve": TaskType(
        "Retrieve Value",
        OracleWeight(coverage=2, diversity=0, specificity=2, interestingness=0),
        [chart_types["scatter"], chart_types["heatmap"]],
    ),
    "correaltion": TaskType(
        "Correlation",
        OracleWeight(coverage=0, diversity=2, specificity=1, interestingness=2),
        [chart_types["scatter"], chart_types["heatmap"]],
    ),
    "compare": TaskType(
        "Compare",
        OracleWeight(coverage=0, diversity=2, specificity=2, interestingness=0),
        [
            chart_types["bar"],
            chart_types["line"],
            chart_types["area"],
            chart_types["scatter"],
            chart_types["heatmap"],
        ],
    ),
    "cluster": TaskType(
        "Cluster",
        OracleWeight(coverage=1, diversity=1, specificity=1, interestingness=-3),
        [chart_types["scatter"], chart_types["heatmap"]],
    ),
    "distribution": TaskType(
        "Characterize Distribution",
        OracleWeight(coverage=2, diversity=2, specificity=1, interestingness=0),
        [
            chart_types["scatter"],
            chart_types["boxplot"],
            chart_types["stripplot"],
            chart_types["bar"],
            chart_types["line"],
            chart_types["area"],
            chart_types["heatmap"],
        ],
    ),
    "anomalies": TaskType(
        "Find Anomalies",
        OracleWeight(coverage=1, diversity=1, specificity=1, interestingness=2),
        [
            chart_types["scatter"],
            chart_types["line"],
            chart_types["boxplot"],
            chart_types["heatmap"],
            chart_types["stripplot"],
        ],
    ),
    "extremum": TaskType(
        "Find Extremum",
        OracleWeight(coverage=1, diversity=1, specificity=1, interestingness=0),
        [chart_types["bar"], chart_types["line"], chart_types["scatter"]],
    ),
    "derived": TaskType(
        "Compute Derived Value",
        OracleWeight(coverage=1, diversity=2, specificity=2, interestingness=1),
        [
            chart_types["bar"],
            chart_types["line"],
            chart_types["scatter"],
            chart_types["pie"],
        ],
    ),
}
