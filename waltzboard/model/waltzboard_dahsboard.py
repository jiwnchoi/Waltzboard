import altair as alt
from waltzboard.model import BaseChart
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class WaltzboardDashboard:
    charts: list[BaseChart]

    def __len__(self):
        return len(self.charts)

    def append(self, chart: BaseChart):
        self.charts.append(chart)
        return self

    def extend(self, charts: list[BaseChart]):
        keys = [c.tokens for c in self.charts]
        new_charts = [c for c in charts if c.tokens not in keys]
        return WaltzboardDashboard(self.charts + new_charts)

    def display(self, width: int = 150, height: int = 150, num_cols: int = 4):
        if self.charts is None:
            return None
        altairs = [
            chart.display().properties(width=width, height=height)
            for chart in self.charts
        ]
        rows: list[alt.HConcatChart] = [
            alt.hconcat(*altairs[i : i + num_cols]).resolve_scale(
                color="independent"
            )
            for i in range(0, len(altairs), num_cols)
        ]
        return alt.vconcat(*rows)
