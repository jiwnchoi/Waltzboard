import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined
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
                    timeUnit=self.altair_token.x.aggregate,
                ),
                y=alt.Y(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    aggregate=self.altair_token.y.aggregate,
                    axis=alt.Axis(format="~s" if self.altair_token.y.type == "quantitative" else Undefined),
                ),
                color=alt.Color(self.altair_token.z.name, type=self.altair_token.z.type),
            )
        )
