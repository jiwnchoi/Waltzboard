import altair as alt
from altair import Chart
from altair.utils.schemapi import UndefinedType
from .base_chart import BaseChart


class ScatterPlot(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_circle()
            .encode(
                alt.X(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                ),
                alt.Y(self.altair_token.y.name, type=self.altair_token.y.type),
                alt.Color(
                    self.altair_token.z.name,
                    type=self.altair_token.z.type,
                    bin=True if self.altair_token.z.aggregate == "bin" else False,
                ),
            )
        )
