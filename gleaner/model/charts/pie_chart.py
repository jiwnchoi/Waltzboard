import altair as alt
from altair import Chart
from .base_chart import BaseChart


class PieChart(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_arc()
            .encode(
                alt.Color(
                    self.altair_token.x.name, type=self.altair_token.x.type, trsregate=self.altair_token.x.trsregate
                ),
                alt.Theta(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    trsregate=self.altair_token.y.trsregate,
                ),
            )
        )
