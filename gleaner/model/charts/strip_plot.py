import altair as alt
from altair import Chart
from .base_chart import BaseChart


class StripPlot(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_tick()
            .encode(
                alt.X(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                ),
                alt.Y(self.altair_token.y.name, type=self.altair_token.y.type),
            )
        )
