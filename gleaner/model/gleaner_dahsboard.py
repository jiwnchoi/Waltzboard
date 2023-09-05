import altair as alt
from gleaner.model import BaseChart
from gleaner.oracle import OracleResult
from dataclasses import dataclass


@dataclass
class GleanerDashboard:
    charts: list[BaseChart]

    def __len__(self):
        return len(self.charts)

    def append(self, chart: BaseChart):
        self.charts.append(chart)

    def extend(self, charts: list[BaseChart]):
        self.charts = charts + self.charts

    def display(self, width: int = 150, height: int = 150, num_cols: int = 4):
        if self.charts is None:
            return None
        altairs = [chart.display().properties(width=width, height=height) for chart in self.charts]
        rows: list[alt.HConcatChart] = [
            alt.hconcat(*altairs[i : i + num_cols]).resolve_scale(color="independent")
            for i in range(0, len(altairs), num_cols)
        ]
        return alt.vconcat(*rows)
