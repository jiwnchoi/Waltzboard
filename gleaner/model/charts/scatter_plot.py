import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined
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
                    axis=alt.Axis(
                        format="~s"
                        if self.altair_token.y.type == "quantitative"
                        else Undefined
                    ),
                ),
                alt.Y(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    axis=alt.Axis(
                        format="~s"
                        if self.altair_token.y.type == "quantitative"
                        else Undefined
                    ),
                ),
                alt.Color(
                    self.altair_token.z.name,
                    type=self.altair_token.z.type,
                    bin=True
                    if self.altair_token.z.aggregate == "bin"
                    else False,
                    legend=alt.Legend(
                        format="~s"
                        if self.altair_token.z.type != "nominal"
                        else Undefined
                    ),
                ),
            )
        )
