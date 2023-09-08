import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined
from .base_chart import BaseChart


class BoxPlot(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_boxplot()
            .encode(
                alt.X(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                ),
                alt.Y(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    axis=alt.Axis(format="~s" if self.altair_token.y.type == "quantitative" else Undefined),
                ),
            )
        )
