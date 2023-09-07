import altair as alt
from altair import Chart
from .base_chart import BaseChart


class LineChart(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_line()
            .encode(
                x=alt.X(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                    timeUnit=self.altair_token.x.trsregate,
                ),
                y=alt.Y(
                    self.altair_token.y.name, type=self.altair_token.y.type, trsregate=self.altair_token.y.trsregate
                ),
                color=alt.Color(self.altair_token.z.name, type=self.altair_token.z.type),
            )
        )
